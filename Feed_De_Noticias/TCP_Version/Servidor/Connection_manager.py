# connection_manager.py
import json

class ConnectionManager:
    def __init__(self):
        self.subscriptions = {}
        self.notices = {}  #Temporariamente inutil
    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
    
                data = json.loads(message)
                command = data.get('command')
                topic = data.get('topic')

                if command == 'subscribe':
                    self.subscribe(client_socket, topic)
                elif command == 'unsubscribe':
                    self.unsubscribe(client_socket, topic)
                elif command == 'publish':
                    title = data.get('title')
                    body = data.get('body')
                    self.publish(topic, title, body)
            except (ConnectionResetError, json.JSONDecodeError):
                break
        
        self.disconnect(client_socket, addr)

    def send_message_for_all(self, topic, title, body):
         for subscriber in self.subscriptions[topic]:
                try:
                    subscriber.sendall(json.dumps({
                        'topic': topic,
                        'title': title,
                        'body': body
                    }).encode('utf-8'))
                except ConnectionResetError:
                    self.unsubscribe(subscriber, topic)
    def publish (self, topic, title, body):
        
        content = {"title": title, "body": body}
        if topic in self.notices:
            self.notices[topic].append(content)
        else:
            self.notices[topic] = [content]
       
        if topic in self.subscriptions:     
           self.send_message_for_all(topic, title, body)
        else:
            self.subscriptions[topic] = []
        self.notices[topic] = [content]
        
    def subscribe(self, client_socket, topic):
        if topic in self.subscriptions:
            if client_socket not in self.subscriptions[topic]:
                self.subscriptions[topic].append(client_socket)
        else:
            self.subscriptions[topic] = [client_socket] #Cpode se inscrever msm que não tenha nenhuma noticia.
        print(f"Cliente {client_socket.getpeername()} se inscreveu no tópico: {topic}")

    def unsubscribe(self, client_socket, topic):
        if topic in self.subscriptions and client_socket in self.subscriptions[topic]:
            self.subscriptions[topic].remove(client_socket)
        print(f"Cliente {client_socket.getpeername()} cancelou a inscrição no tópico: {topic}")

    def disconnect(self, client_socket, addr):
        print(f"[*] Conexão de {addr} encerrada.")
        client_socket.close()