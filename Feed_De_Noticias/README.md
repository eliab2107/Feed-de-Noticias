# Feed de Notícias Contínuo (Cliente-Servidor TCP)

Este projeto implementa uma aplicação **cliente-servidor** usando **socket TCP**, onde os clientes recebem notícias em tempo real de acordo com as categorias nas quais estão inscritos.

---

## Funcionalidades

* O **servidor** mantém categorias de notícias (ex.: tecnologia, política, esportes, cultura).
* As notícias são cadastradas por um **editor**, que publica novas entradas no sistema.
* Assim que uma nova notícia é publicada, o servidor envia automaticamente para todos os clientes inscritos naquela categoria.
* Os **clientes** podem:

  * Se conectar ao servidor.
  * Escolher categorias de interesse (`SUBSCRIBE <categoria>`).
  * Cancelar a inscrição em categorias (`UNSUBSCRIBE <categoria>`).
* O servidor gerencia várias conexões simultâneas e envia apenas notícias das categorias que o cliente faz parte.

---

## Pré-requisitos

Antes de rodar o projeto, é necessário ter o python instalado!

Instalar as dependências:

```bash
pip install -r requirements.txt
```

---

## Como Executar

A aplicação deve ser iniciada em **três etapas**: **Servidor**, **Editor** e **Cliente(s)**.

### 1. Iniciar o Servidor

No terminal, dentro da pasta raiz do projeto:

```bash
python Feed_De_Noticias/Servidor/Server.py
```

O servidor ficará ativo aguardando as conexões de clientes e do editor.

### 2. Iniciar o Editor

Em outro terminal:

```bash
python Feed_De_Noticias/Editor/Editor.py
```

O editor será responsável por publicar notícias informando **topic, title e body**.
Essas notícias serão enviadas imediatamente para os clientes inscritos naquele topic.

### 3. Conectar um Cliente

Em outro terminal (um ou mais clientes podem ser iniciados):

```bash
python Feed_De_Noticias/Cliente/Client.py
```

O cliente poderá interagir enviando comandos como:

* `SUBSCRIBE tecnologia` → Inscreve-se na categoria **tecnologia**.
* `UNSUBSCRIBE politica` → Cancela a inscrição na categoria **política**.
* `EXIT` → Sair da aplicação. (através do botão da interface)

---

## Observações

* O projeto usa **sockets TCP persistentes** para manter a comunicação em tempo real.
* Suporta **múltiplos clientes simultâneos**.
* O editor é essencial para o funcionamento, pois ele publica as notícias que serão distribuídas.

---

## Equipe 04
* Alice Vitória
* Eliab Bernardino
