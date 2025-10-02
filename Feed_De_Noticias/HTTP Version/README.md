📡 Sistema de Feed Distribuído com HTTP + SSE

Este projeto implementa um sistema de feed de notícias em tempo real utilizando HTTP e a técnica de Server-Sent Events (SSE).

O objetivo é demonstrar como construir, do zero, um sistema distribuído onde múltiplos clientes podem se inscrever em tópicos de interesse e receber atualizações automaticamente sempre que novas mensagens forem publicadas, sem precisar ficar enviando requisições repetidamente.

🚀 Como funciona o sistema
🔹 Servidor (server.py)

Implementado usando a biblioteca padrão do Python (http.server e ThreadingHTTPServer).

Permite conexões HTTP normais, mas fornece suporte especial a SSE para streaming contínuo de eventos.

Cada cliente que conecta em /stream?topic=... recebe:

Um UUID (client_id) único, enviado no primeiro evento.

Eventos subsequentes de acordo com os tópicos em que estiver inscrito.

Mantém:

Uma lista de clientes ativos, cada um associado a uma fila (queue.Queue) para envio de mensagens.

Um dicionário de tópicos, cada um mapeando os clientes inscritos.

Endpoints principais:

GET /stream?topic=... → abre uma conexão SSE, entrega client_id e começa a enviar mensagens em tempo real.

POST /publish → publica uma mensagem em um tópico; todos os inscritos recebem.

PUT / → gerencia inscrições:

{"action": "subscribe", "client_id": "...", "topic": "..."} → inscreve cliente em tópico.

{"action": "unsubscribe", "client_id": "...", "topic": "..."} → remove cliente de tópico.

🔹 Cliente Subscriber (subscriber_client.py)

Interface gráfica feita com Tkinter.

Funcionalidades:

Conectar ao servidor informando um tópico inicial.

Receber em tempo real os eventos de feed via SSE.

Visualizar no painel todas as atualizações recebidas.

Inscrever-se em novos tópicos (PUT /subscribe).

Cancelar inscrição em tópicos (PUT /unsubscribe).

Primeira mensagem recebida do servidor contém o client_id, que é salvo para futuras operações.

🔹 Cliente Publisher (publisher_client.py) (opcional)

Também em Tkinter.

Permite enviar mensagens para o servidor via POST /publish.

O usuário preenche:

Título

Tópico

Corpo da mensagem

O servidor, ao receber, envia essa mensagem a todos os clientes inscritos no tópico.

📋 Requisitos

Python 3.8+

Nenhuma dependência externa é obrigatória (apenas a biblioteca padrão).

Para rodar as GUIs (Tkinter), é necessário ter suporte gráfico no ambiente.

▶️ Como rodar

Clonar o repositório (ou copiar os arquivos para uma pasta).

git clone https://github.com/eliab2107/Feed-de-Noticias.git


Iniciar o servidor na pasta servidor execute:

python server.py


O servidor abrirá em http://localhost:8080.

Rodar um cliente Subscriber na pasta Cliente execute:

python client.py


Digite um tópico inicial.

Clique em Conectar.

Use os botões Inscrever e Desinscrever para gerenciar tópicos.

Rodar um cliente Publisher(Editor), na pasta Editor execute:

python editor.py

Informe tópico, título e corpo.

Clique em Publicar para enviar ao servidor.

🔧 Fluxo esperado

O cliente Subscriber conecta ao servidor, recebendo seu client_id.

O cliente pode se inscrever em múltiplos tópicos (usando PUT /subscribe).

O cliente Publisher (ou qualquer requisição POST /publish) envia mensagens em um tópico.

Todos os inscritos nesse tópico recebem o evento em tempo real, sem precisar atualizar ou enviar novas requisições.

🧩 Estrutura de Mensagens

Primeira mensagem ao conectar (client_id):

{
  "client_id": "550e8400-e29b-41d4-a716-446655440000"
}


Mensagem publicada (broadcast para inscritos):

{
  "topic": "tecnologia",
  "title": "Novo framework Python",
  "body": "Lançada versão beta do framework X para desenvolvimento web."
}

📚 Conceitos envolvidos

HTTP: protocolo base de comunicação.

TCP: camada de transporte que garante entrega confiável.

SSE (Server-Sent Events): técnica baseada em HTTP que mantém a conexão aberta para envio contínuo de dados do servidor → cliente.

Pub/Sub (Publisher/Subscriber): modelo de comunicação onde clientes se inscrevem em tópicos e recebem mensagens publicadas por outros.

✨ Pontos fortes da solução

✅ Somente biblioteca padrão do Python

✅ Suporte a múltiplos clientes simultâneos (via ThreadingHTTPServer)

✅ Estrutura extensível para novos endpoints

✅ Modelo Pub/Sub real em HTTP, sem precisar de WebSockets

📌 Esse projeto foi desenvolvido como parte de um estudo em Plataformas Distribuídas, no contexto de um mestrado em Ciência da Computação.