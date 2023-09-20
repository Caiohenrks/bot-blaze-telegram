# Utilizar uma imagem base de Python
FROM python:3.10

# Definir diretório de trabalho no container
WORKDIR /usr/src/app

# Copiar o arquivo de requisitos para o container
COPY requirements.txt ./

# Instalar os pacotes necessários
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código fonte para o diretório de trabalho
COPY . .

# Comando para executar o script
CMD [ "python", "./bot.py" ]

