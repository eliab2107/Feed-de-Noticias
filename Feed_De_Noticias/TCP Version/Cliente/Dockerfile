# Usa a mesma imagem base leve
FROM python:3.9-slim-buster

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do cliente
COPY . .

# Comando para iniciar o cliente
# Use "-u" para garantir que a saída do Python seja exibida imediatamente
# (útil para ver o que está acontecendo no terminal)
CMD ["python", "-u", "client.py"]