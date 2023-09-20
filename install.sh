#!/bin/bash

curl -s -X POST https://api.telegram.org/bot6117230868:AAFMYEJZIKAlocyZjW2Q8OiOndmBYSulOLo/sendMessage -d chat_id=-4010498931 -d text="INICIANDO BOT"

# Verificar se a imagem existe
image_exists=$(docker images -q bot-blaze-dev)

# Se a imagem existir, removê-la
if [ ! -z "$image_exists" ]; then
  echo "Removendo a imagem existente..."
  docker rmi -f bot-blaze-dev
fi

# Construir a nova imagem
echo "Construindo a nova imagem..."
docker build -t bot-blaze-dev .

# Verificar se o container existe
container_exists=$(docker ps -a -q --filter name=bot-blaze-dev)

# Se o container existir, removê-lo
if [ ! -z "$container_exists" ]; then
  echo "Removendo o container existente..."
  docker rm -f bot-blaze-dev
fi

# Executar o novo container
echo "Executando o novo container..."
docker run -d --name bot-blaze-dev --restart always bot-blaze-dev

