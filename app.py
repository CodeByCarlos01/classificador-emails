from sklearn.linear_model import SGDClassifier
from imap_tools import MailBox, AND, NOT, OR
from sklearn import cluster
import pandas as pd
import numpy as np
import time
import fun
import os

# Esta função chamada 'adjustClassifier' recebe um argumento 'categoria'.
def adjustClassifier(categoria):
    # Define a pasta de destino para o e-mail atual como a categoria fornecida.
    meu_email.folder.set(f"[{categoria}]")

    # Recupera e-mails com base em suas características, dependendo da categoria.
    # Se a categoria for "Spam", procura por e-mails de outras categorias. Caso contrário, a mesma coisa.
    emails = meu_email.fetch(OR(AND(subject="[URGENTE]"), AND(subject="[IMPORTANTE]"), AND(subject="[HABITUAL]"))) if categoria == "Spam" else meu_email.fetch(NOT(subject=f"[{categoria.upper()}]"))

    # Converte os e-mails recuperados em uma lista.
    lista = list(emails)

    # Verifica se há e-mails na lista e se a lista é diferente da lista de ajustes passados da categoria.
    if len(lista) > 0 and lista != lista_ajustes[categoria]:
        # Cria um DataFrame vazio chamado 'df_ajuste' com uma coluna chamada 'conteudo'.
        df_ajuste = pd.DataFrame(columns=['conteudo'])
        i = 0 # Inicializa um contador.
        # Itera sobre os e-mails na lista.
        for elemento in lista:
            if elemento not in lista_ajustes[categoria]:
                # Adiciona o conteúdo do e-mail ao DataFrame 'df_ajuste'.
                df_ajuste.loc[i] = [elemento.text]
                i += 1
        try:
            # Trata o DataFrame 'df_ajuste' usando a função 'treatData' do módulo 'fun'.
            final_df_ajuste = fun.treatData(df_ajuste)
            # Ajusta as colunas do DataFrame 'final_df_ajuste' usando a função 'adjustColumns' do módulo 'fun'.
            final_df_ajuste = fun.adjustColumns(final_df_ajuste, final_df_treino)
        except Exception as e:
            return
        
        # Encontra o cluster correspondente à categoria atual no dicionário 'categorias'.
        for chave, valor in categorias.items():
            if valor == categoria:
                cluster = chave
                break

        # Ajusta o classificador com os dados do DataFrame 'final_df_ajuste'.
        classifier.partial_fit(final_df_ajuste.fillna(0), np.array([cluster]*len(df_ajuste)))
        # Atualiza a lista de ajustes para a categoria atual.
        lista_ajustes[categoria] = lista

# Esta função verifica a existência de pastas de categorias de e-mail e as cria se não existirem.
# Em seguida, chama a função 'adjustClassifier' para ajustar o classificador com os e-mails dessa categoria.
def verificarPastas():
    if meu_email.folder.exists('[Spam]') == False: meu_email.folder.create('[Spam]')
    else: adjustClassifier("Spam")
    if meu_email.folder.exists('[Habitual]') == False: meu_email.folder.create('[Habitual]')
    else: adjustClassifier("Habitual")
    if meu_email.folder.exists('[Importante]') == False: meu_email.folder.create('[Importante]')
    else: adjustClassifier("Importante")
    if meu_email.folder.exists('[Urgente]') == False: meu_email.folder.create('[Urgente]')
    else: adjustClassifier("Urgente")

print("Entrando no Email...")
# Dados de Email
##############################
usuario = "" # Definir email
senha = "" # Definir senha de app do email
server_imap = "imap.gmail.com"
server_smtp = "smtp.gmail.com"

# Configuração da caixa de correio de e-mail usando o protocolo IMAP.
# O objeto 'meu_email' representa a caixa de correio e permite interagir com a conta de e-mail especificada.
meu_email = MailBox(server_imap).login(usuario, senha)

# Configuração do modelo de cluster K-Means.
kmeans = cluster.KMeans(n_clusters = 4, init = 'k-means++', n_init = 1, random_state = 42)

print("Carregando Base de Dados... [AGUARDE]")
# Verifica se o arquivo 'datasets/data.csv' existe.
if os.path.exists('datasets/data.csv'):
    # Se o arquivo existe, lê o conteúdo do arquivo CSV em um DataFrame pandas.
    df_treino = pd.read_csv('datasets/data.csv')
    # Garante que a coluna 'conteudo' seja tratada como uma string.
    df_treino['conteudo'] = df_treino['conteudo'].astype(str)
else:
    # Se o arquivo não existe, coleta até 300 e-mails da caixa de correio.
    lista_emails = meu_email.fetch(reverse=True, limit=300)
    l = list(lista_emails)
    # Cria um DataFrame vazio chamado 'df_treino' com uma coluna chamada 'conteudo'.
    df_treino = pd.DataFrame(columns=['conteudo'])
    # Itera sobre os e-mails coletados e adiciona seus conteúdos ao DataFrame.
    for i in range(len(l)):
        df_treino.loc[i] = [l[i].text]
    # Salva o DataFrame em um arquivo CSV chamado 'datasets/data.csv' para uso futuro.
    df_treino.to_csv('datasets/data.csv', index=False)

print("Construindo Agrupador...")
# Pré-processamento dos dados de treinamento utilizando a função 'treatData' do módulo 'fun'.
final_df_treino = fun.treatData(df_treino)
# Ajusta o modelo K-Means aos dados de treinamento pré-processados.
kmeans.fit(final_df_treino)

print("Construindo Classificador...")
# Define um dicionário 'categorias' que mapeia os rótulos de cluster (0, 1, 2, 3) para categorias de e-mail.
categorias = {0: "Spam", 1: "Urgente", 2: "Habitual", 3: "Importante"}
# Cria um dicionário 'lista_ajustes' que armazena listas vazias para cada categoria.
lista_ajustes = {"Spam": [], "Urgente": [], "Habitual": [], "Importante": []}
# Inicializa um classificador do tipo SGD (Gradiente Descendente Estocástico) com a função de perda 'log' 
# e um máximo de 1000 iterações.
classifier = SGDClassifier(loss='log', max_iter=1000)
# Treina o classificador utilizando os dados de treinamento 'final_df_treino' (que deve conter os dados pré-processados)
# e os rótulos de cluster 'kmeans.labels_'.
classifier.fit(final_df_treino.fillna(0), kmeans.labels_)

# Cria um novo DataFrame vazio chamado 'df_teste' com uma coluna chamada 'conteudo'.
df_teste = pd.DataFrame(columns=['conteudo'])

print("Aplicacao em Funcionamento...")
while True:
    try:
        # Define a pasta de destino como 'INBOX' para buscar novos e-mails não lidos.
        meu_email.folder.set('INBOX')
        # Recupera novos e-mails não lidos.
        novos_emails = meu_email.fetch(AND(seen=False))
        l = list(novos_emails)
        # Se houver novos e-mails não lidos.
        if len(l) > 0:
            # Verifica, cria pastas de categorias e ajusta classificador se necessário.
            verificarPastas()
            # Itera sobre os novos e-mails.
            for i in range(len(l)):
                # Adiciona o conteúdo do e-mail ao DataFrame 'df_teste'.
                df_teste.loc[0] = [l[i].text]
                try:
                    # Pré-processa o DataFrame 'df_teste'.
                    final_df_teste = fun.treatData(df_teste)
                    final_df_teste = fun.adjustColumns(final_df_teste, final_df_treino)
                    # Classifica o e-mail com base no modelo 'classifier'.
                    categoria = categorias[int(classifier.predict(final_df_teste))]
                except Exception as e:
                    categoria = "Spam"
                # Se a categoria for "Spam", move o e-mail para a pasta "[Spam]".
                if categoria == "Spam":
                    meu_email.folder.set('INBOX')
                    meu_email.move(meu_email.uids(AND(uid=l[i].uid)), "[Spam]")
                    continue
                # Caso contrário, envia um novo e-mail resumido para a pasta correspondente.
                fun.sendEmail(server_smtp, usuario, senha, l[i].from_, f"[{categoria.upper()}] {l[i].subject}", l[i].text)
                meu_email.folder.set('INBOX')
                meu_email.move(meu_email.uids(AND(from_=usuario, to=usuario)), f"[{categoria}]")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    # Aguarda um intervalo de tempo (10 segundos) antes de verificar novamente.
    time.sleep(10)