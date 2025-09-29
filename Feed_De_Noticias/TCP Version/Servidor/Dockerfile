# Usa uma imagem Python leve e pequena
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para a imagem antes de instalar as dependências
# Isso aproveita o cache do Docker, acelerando futuras builds
COPY requirements.txt .

# Instala as dependências Python
# O --no-cache-dir reduz o tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da sua aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o servidor irá escutar
# É mais uma documentação, o docker-compose lida com a exposição real
EXPOSE 5000

# Comando para iniciar o servidor quando o container for executado
CMD ["python", "server.py"]