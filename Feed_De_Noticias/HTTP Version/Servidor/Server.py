import socket
from threading import Thread, Lock
from LittleParser import Little_Parser
import json

HOST = 'localhost'
PORT = 8080
class client_info():
    def __init__(self, socket, addr):
        self.conn = socket
        self.addr = addr
        self.subscriptions = []
        
class ServerApp():
    def __init__(self):
        self.clients = {}
        self.topics = {}
        self.endpoints = {"/subscribe": self.handle_subscribe, "/unsubscribe": self.handle_unsubscribe, "/publish": self.handle_publish, "/hello": self.hello}  
        self.clients_lock = Lock()
        self.topics_lock = Lock()
        
        self.editor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.editor_socket.bind((HOST, PORT))
        self.editor_socket.listen()
        print(f"Server listening for clients on {HOST}:{PORT}")
        Thread(target=self.run_server).start()

    
    def hello(self, client, message):
       print(f"Hello from {client.addr}: {message.get_body()}")
       
       
    def run_server(self):
        while True:
            print("Connection accepted")
            socket, addr = self.editor_socket.accept()
            print(f"Connected by {addr}")
            self.handle_client(socket, addr)
    
        
    def handle_subscribe(self):
        pass
    
    def handle_unsubscribe(self):
        pass
    
    def handle_publish(self):
        pass
    
    def handle_client(self, socket, addr):
        
        if addr not in self.clients:
            self.clients[addr] = client_info(socket, addr)
        message = Little_Parser(socket.recv(1024).decode('utf-8'))    
        print(f"Received from {addr}: {message.get_body()}")
        print(f"Headers: {message.get_headers()}")
        self.endpoints.get(message.get_path(), lambda c, m: None)(self.clients[addr], message)

if __name__ == "__main__":
    server = ServerApp()
   
    
    
    