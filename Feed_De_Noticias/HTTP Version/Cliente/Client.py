import socket
from threading import Thread
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox
from LittleParser import Little_Parser, Builder_Message

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

class ClientApp():
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Thread(target=self.run_client(), daemon=True).start()
        
        self.create_gui()

    def run_client(self): 
        self.client_socket.connect((SERVER_HOST, SERVER_PORT)) 
        self.client_socket.sendall(Builder_Message(body={"name": "123"}).build_request("POST", "/hello").encode('utf-8'))
        while True:         

            json_notice, _ = self.client_socket.recvfrom(1024)
            try:
                data = json.loads(json_notice.decode('utf-8'))
                topic = data.get('topic')
                title = data.get('title')
                body = data.get('body')
                self.feed_area.insert(tk.END, f" ==================== NEW NOTICE ====================\n[TÓPICO]: {topic}\n[TITULO]: {title}\n[RESUMO]: {body}\n\n")
                self.feed_area.see(tk.END) 
            except Exception as e :
                self.feed_area.insert(tk.END, f"Mensagem recebida: {json_notice}\n Erro: {e}\n")
            
            
    def send_command(self, topic, comand):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Atenção", "Por favor, digite um nome de tópico.")
            return

        message = {
            "command": comand,
            "topic": topic,
            "ip": self.ip_address,
            "port": self.port
        }
        try:
            self.client_socket.sendto(json.dumps(message).encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        except Exception as e:
            messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao enviar a mensagem: {e}")
        
        
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Cliente Feed de Notícias")
        self.root.geometry("600x500")

        # Frame principal
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Campo de entrada para o tópico
        self.topic_frame = tk.Frame(self.main_frame)
        self.topic_frame.pack(fill=tk.X, pady=5)
        tk.Label(self.topic_frame, text="Tópico:").pack(side=tk.LEFT, padx=(0, 5))
        self.topic_entry = tk.Entry(self.topic_frame, width=30)
        self.topic_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Botões de ação
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)
        subscribe_button = tk.Button(self.button_frame, text="Inscrever", command=lambda: self.send_command(self.topic_entry.get().strip(), "subscribe"))
        subscribe_button.pack(side=tk.LEFT, padx=5)
        unsubscribe_button = tk.Button(self.button_frame, text="Desinscrever", command=lambda: self.send_command(self.topic_entry.get().strip(), "unsubscribe"))
        unsubscribe_button.pack(side=tk.LEFT, padx=5)

        # Área de exibição do feed
        tk.Label(self.main_frame, text="Feed de Notícias:").pack(pady=(10, 0), anchor='w')
        self.feed_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, state=tk.NORMAL)
        self.feed_area.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.root.mainloop()
        
if __name__ == "__main__":
    client = ClientApp()