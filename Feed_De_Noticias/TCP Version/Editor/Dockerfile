# Usa a mesma imagem base
FROM python:3.9-slim-buster

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do editor
COPY . .

# Comando para iniciar o editor
CMD ["python", "-u", "editor.py"]