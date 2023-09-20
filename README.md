# Classificador de E-mails
Este projeto consiste em um classificador de e-mails que organiza mensagens em categorias como `Spam`, `Urgente`, `Habitual` e `Importante`. O classificador utiliza técnicas de processamento de linguagem natural (PLN) e aprendizado de máquina para atribuir automaticamente categorias aos e-mails com base no seu conteúdo.
## Funcionalidades
- Classifica automaticamente os e-mails em quatro categorias: Spam, Urgente, Habitual e Importante.
- Usa o modelo de cluster K-Means para agrupar e-mails semelhantes.
- Implementa um classificador baseado em gradiente descendente estocástico (SGD) para atribuir categorias.
- Realiza o pré-processamento dos e-mails, incluindo a remoção de stopwords, stemming e TF-IDF.
- Envia e-mails para as pastas correspondentes.
- Permite que o usuário faça ajustes no classificador para uma classificação mais personalizada.
## Pré-requisitos
- Python 3.x
- Bibliotecas Python: `scikit-learn`, `imap-tools`, `pandas`, `numpy`, `nltk`, `unidecode`
### 1. scikit-learn:
```sh
pip install scikit-learn
```
### 2. imap-tools:
```sh
pip install imap-tools
```
### 3. pandas:
```sh
pip install pandas
```
### 4. numpy:
```sh
pip install numpy
```
### 5. nltk (Natural Language Toolkit):
```sh
pip install nltk
```
Depois de instalar o nltk, é necessário baixar os dados adicionais usando os seguintes comandos:
```sh 
python
```
```sh
import nltk
```
```sh
nltk.download()
```
Execute um comando por vez.
### 6. unidecode:
```sh
pip install unidecode
```
## Configuração
Antes de executar o projeto, é necessário configurar as seguintes variáveis no arquivo __app.py__:

- `usuario`: Insira seu endereço de e-mail.
- `senha`: Insira a senha de aplicativo para o seu e-mail.
- `server_imap`: Insira o servidor IMAP do seu provedor de e-mail (por padrão, é configurado para o Gmail).
- `server_smtp`: Insira o servidor SMTP do seu provedor de e-mail (por padrão, é configurado para o Gmail).

### Explicando como criar senha de App
[![Explicando como criar senha de App](https://i.ytimg.com/vi/ZqFaFEIqTaE/hqdefault.jpg?sqp=-oaymwE2COADEI4CSFXyq4qpAygIARUAAIhCGAFwAcABBvABAfgB_gmAArQFigIMCAAQARh_ICIoGzAP&rs=AOn4CLB0wDv_2N1LFLbGPAT83JW33u6zUw)](https://www.youtube.com/watch?v=ZqFaFEIqTaE)
## Uso
1. Execute o arquivo __app.py__ para iniciar o classificador de e-mails.
2. O classificador buscará novos e-mails na `Caixa de Entrada` e os classificará automaticamente.
3. Os e-mails serão movidos para as pastas correspondentes com base na classificação.

Certifique-se de manter o projeto em execução para que ele continue a classificar e-mails em tempo real.
## Ajuste
A aplicação permite o usuário fazer ajustes na classificação dos e-mails, simplesmente movendo-os entre pastas. Essa capacidade é muito valiosa e oferece aos usuários o controle e a personalização necessários para garantir que os e-mails sejam categorizados de acordo com suas preferências individuais. Proporcionando mais flexibilidade e aprimoramento contínuo.
## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou relatar problemas.

*Muito obrigado por usar nosso aplicativo e boa classificação de e-mails!* 📧✨
