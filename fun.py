import pandas as pd

# Corpus Processing
import re
import nltk.corpus
from nltk.stem                        import RSLPStemmer
from nltk.tokenize                    import word_tokenize
from unidecode                        import unidecode
from sklearn.feature_extraction.text  import TfidfVectorizer

# SMTP Server
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# remove uma lista de palavras (ou seja, stopwords) de uma lista tokenizada.
def removeWords(listOfTokens, listOfWords):
    return [token for token in listOfTokens if token not in listOfWords]

# aplica-se a uma lista de palavras tokenizadas
def applyStemming(listOfTokens, stemmer):
    return [stemmer.stem(token) for token in listOfTokens]

# remove todas as palavras compostas por menos de 2 ou mais de 21 letras
def twoLetters(listOfTokens):
    twoLetterWord = []
    for token in listOfTokens:
        if len(token) <= 2 or len(token) >= 21:
            twoLetterWord.append(token)
    return twoLetterWord

# processa o conteúdo do email, removendo tudo que for desnecessário
def processCorpus(corpus, language):   
    stopwords = nltk.corpus.stopwords.words(language)
    param_stemmer = RSLPStemmer()
    other_words = [line.rstrip('\n') for line in open('lists/stopwords_scrapmaker.txt')] # Carregar arquivo .txt linha por linha

    for document in corpus:
        index = corpus.index(document)
        corpus[index] = corpus[index].replace(u'\ufffd', '8')   # Substitui o símbolo ASCII ' ' por '8'
        corpus[index] = corpus[index].replace(',', '')          # remove vírgulas
        corpus[index] = corpus[index].rstrip('\n')              # Remove quebras de linha
        corpus[index] = corpus[index].casefold()                # Torna todas as letras minúsculas
        
        corpus[index] = re.sub('\W_',' ', corpus[index])        # remove caracteres especiais e deixa apenas palavras
        corpus[index] = re.sub("\S*\d\S*"," ", corpus[index])   # remove números e palavras concatenadas com números IE h4ck3r. Remove nomes de estradas como BR-381.
        corpus[index] = re.sub("\S*@\S*\s?"," ", corpus[index]) # remove e-mails e menções (palavras com @)
        corpus[index] = re.sub(r'http\S+', '', corpus[index])   # remove URLs com http
        corpus[index] = re.sub(r'www\S+', '', corpus[index])    # remove URLs com www

        listOfTokens = word_tokenize(corpus[index], language ='portuguese')
        twoLetterWord = twoLetters(listOfTokens)

        listOfTokens = removeWords(listOfTokens, stopwords)
        listOfTokens = removeWords(listOfTokens, twoLetterWord)
        listOfTokens = removeWords(listOfTokens, other_words)
        
        listOfTokens = applyStemming(listOfTokens, param_stemmer)
        listOfTokens = removeWords(listOfTokens, other_words)

        corpus[index]   = " ".join(listOfTokens)
        corpus[index] = unidecode(corpus[index])

    return corpus

def treatData(df):
    # Realiza o PNL(Process Natural Language)
    df.columns = map(str.lower, df.columns)
    conteudo = df['conteudo'].tolist()
    conteudo = processCorpus(conteudo, 'portuguese')

    # Aplica o TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(conteudo)
    tf_idf = pd.DataFrame(data = X.toarray(), columns=vectorizer.get_feature_names_out())
    final_df = tf_idf

    return final_df

# Esta função chamada 'adjustColumns' recebe dois DataFrames como entrada: 'df_teste' e 'df_traino'.
def adjustColumns(df_teste, df_traino):
    
    # Calcula a diferença entre as colunas de 'df_traino' e 'df_teste' usando conjuntos (set).
    colunas_ausentes = set(df_traino.columns) - set(df_teste.columns)

    # Cria um dicionário 'data' com as colunas ausentes como chaves e listas contendo zeros como valores.
    data = {col: [0] for col in colunas_ausentes}

    # Concatena o DataFrame 'df_teste' com um novo DataFrame criado a partir do dicionário 'data',
    # adicionando as colunas ausentes ao 'df_teste'.
    df_teste = pd.concat([df_teste, pd.DataFrame(data)], axis=1)

    # Garante que o DataFrame 'df_teste' tenha exatamente as mesmas colunas que 'df_traino',
    # reordenando as colunas, se necessário.
    df_teste = df_teste[df_traino.columns]

    # Retorna o DataFrame 'df_teste' com as colunas ajustadas.
    return df_teste

def sendEmail(server, username, password, from_, subject, message):
    # Configurações do servidor SMTP
    smtp_server = server
    smtp_port = 587  # Porta SMTP padrão para comunicação segura (TLS)
    smtp_username = username
    smtp_password = password

    # Crie um objeto MIMEMultipart para compor a mensagem
    msg = MIMEMultipart()
    msg['From'] = from_
    msg['To'] = username
    msg['Subject'] = Header(subject, 'utf-8').encode()

    # Corpo da mensagem
    mensagem = f"Enviado por: {from_}\n\n{message}"
    msg.attach(MIMEText(mensagem, 'plain'))

    # Inicialize o servidor SMTP
    smtp = smtplib.SMTP(smtp_server, smtp_port)

    # Inicie a conexão TLS para segurança
    smtp.starttls()

    # Faça login no servidor SMTP
    smtp.login(smtp_username, smtp_password)

    # Envie o email
    smtp.sendmail(smtp_username, smtp_username, msg.as_string())

    # Feche a conexão SMTP
    smtp.quit()