from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock, Thread
import time

# Lista global de clientes conectados
clients = []
clients_lock = Lock()


class Topic:
    def __init__(self, title):
        self.users = []
        self.notices = []
        self.title = ""
        
class TopicsManager:
    def __init__(self):
        self.topics = {}

    def subscribe(self, topic, client):
        if topic not in self.topics:
            self.topics[topic] = Topic(topic)
        if client not in self.topics[topic]:
            self.topics[topic].users.append(client)

    def unsubscribe(self, topic, client):
        if topic in self.topics and client in self.topics[topic].users:
            self.topics[topic].users.remove(client)
        

    def publish_notice(self, topic, notice):
        if topic in self.topics:
            self.topics[topic].notices.append(notice)
            for client in self.topics[topic].users:
                client.sendall(notice)

class SSEHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/stream":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            self.topics_manager = TopicsManager()            
            
            with clients_lock:
                clients.append(self.wfile)

            try:
                while True:
                    self.wfile.write(b": keep-alive\n\n")
                    self.wfile.flush()
                    time.sleep(10)
            except (ConnectionResetError, BrokenPipeError):
                
                with clients_lock:
                    if self.wfile in clients:
                        clients.remove(self.wfile)
        else:
            self.send_response(404)
            self.end_headers()
            
    def do_POST(self):
        if self.path == "/subscribe":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            topic = post_data.decode('utf-8')
            self.topics_manager.subscribe(topic, self.wfile)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Subscribed to topic")
            
        elif self.path == "/unsubscribe":
            pass
        
        elif self.path == "/publish":
            pass 

def broadcast(message: str):
    data = f"data: {message}\n\n".encode("utf-8")
    with clients_lock:
        disconnected = []
        for client in clients:
            try:
                client.write(data)
                client.flush()
            except (ConnectionResetError, BrokenPipeError):
                disconnected.append(client)
        for d in disconnected:
            clients.remove(d)

def event_generator():
    i = 0
    while True:
        time.sleep(5)
        msg = f"Broadcast {i}"
        print(f"Enviando: {msg}")
        #  broadcast(msg)
        i += 1

if __name__ == "__main__":
    server = ThreadingHTTPServer(("localhost", 8080), SSEHandler)
    print("Servidor SSE rodando em http://localhost:8080/stream")

    # Thread que gera mensagens periódicas
    Thread(target=event_generator, daemon=True).start()

    server.serve_forever()
