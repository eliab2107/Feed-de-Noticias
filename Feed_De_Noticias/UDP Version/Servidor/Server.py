import socket
from threading import Thread, Lock
import json

HOST = 'localhost'
CLIENT_PORT = 5000
EDITOR_PORT = 6000

class ServerApp():
    def __init__(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client.bind((HOST, CLIENT_PORT))
        self.socket_editor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_editor.bind((HOST, EDITOR_PORT))
        self.clients_subscriptions = {}
        self.theme_notices = {}    
        self.subscription_lock = Lock()
        self.notice_lock = Lock()
   
    
    def listen_editors(self):
        print("Aguardando mensagens dos editores...")
        print(f"Servidor ouvindo em {HOST}:{EDITOR_PORT} para editores")
        while True: 
            json_notice, editor_addr = self.socket_editor.recvfrom(1024)
            try:
                data = json.loads(json_notice.decode('utf-8'))
                topic = data.get('topic')
                title = data.get('title')
                body = data.get('body')
            except json.JSONDecodeError:
                print("Erro ao decodificar JSON")
            self.publish_notice(topic=topic, title=title, body=body)
            print(f"[*] Mensagem recebida de {editor_addr[0]}:{editor_addr[1]}")
    
            
    def listen_clients(self):
        while True:  
            print(f"Servidor ouvindo em {HOST}:{CLIENT_PORT} para clientes")
            json_comand, client_addr = self.socket_client.recvfrom(1024)
            try:
                data = json.loads(json_comand.decode('utf-8'))
                command = data.get('command')
                topic   = data.get('topic')
                ip      = data.get('ip')
                port    = data.get('port')
                client_addr = (ip, port)
                if command == 'subscribe':
                    self.add_subscription(topic, client_addr)
                elif command == 'unsubscribe':
                    self.remove_subscription(topic, client_addr)
            except json.JSONDecodeError:
                print("Erro ao decodificar JSON")
            print(f"[*] Mensagem recebida de {client_addr[0]}:{client_addr[1]}")
        
     
    def add_subscription(self, topic, client_addr):
        with self.subscription_lock:
            print(self.clients_subscriptions)
            try:
                if topic not in self.clients_subscriptions:
                    self.clients_subscriptions[topic] = []
                if client_addr not in self.clients_subscriptions[topic]:
                    self.clients_subscriptions[topic].append(client_addr)
                    print(f"Cliente {client_addr} inscrito no tópico '{topic}'")
                else:
                    print(f"Cliente {client_addr} já está inscrito no tópico '{topic}'")
            except Exception as e:
                print(f"Erro ao adicionar inscrição: {e}")
    
    def remove_subscription(self, topic, client_addr):
        with self.subscription_lock:
            try:
                if topic in self.clients_subscriptions and client_addr in self.clients_subscriptions[topic]:
                    self.clients_subscriptions[topic].remove(client_addr)
                    print(f"Cliente {client_addr} desinscrito do tópico '{topic}'")
                else:
                    print(f"Cliente {client_addr} não está inscrito no tópico '{topic}'")
            except Exception as e:
                print(f"Erro ao remover inscrição: {e}")


    def publish_notice(self, topic, title, body):
        with self.notice_lock:
            try:
                if topic not in self.theme_notices:
                    self.theme_notices[topic] = []
                self.theme_notices[topic].append({  "title": title, "body": body})
                print(f"Notícia publicada no tópico '{topic}': {title}")
            except Exception as e:
                print(f"Erro ao publicar notícia: {e}")
            
        with self.subscription_lock:   
            try:                 
                if topic in self.clients_subscriptions:
                    for client_addr in self.clients_subscriptions[topic]:
                        message = json.dumps({"topic":topic, "title":title, "body":body}).encode('utf-8')
                        self.socket_client.sendto(message, client_addr)
                        print(f"Notícia enviada para o cliente {client_addr}")
            except Exception as e:
                print(f"Erro ao enviar notícia para clientes: {e}")


if __name__ == "__main__":
    server = ServerApp()
      
    editor_thread = Thread(target=server.listen_editors)
    client_thread = Thread(target=server.listen_clients)
    
    editor_thread.start()
    client_thread.start()
    
    
    