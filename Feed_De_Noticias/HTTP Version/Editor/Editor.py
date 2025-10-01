import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

SERVER_URL = "http://localhost:8080"

class PublisherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Publisher Client")

        # Campos de entrada
        tk.Label(root, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = tk.Entry(root, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(root, text="Tópico:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.topic_entry = tk.Entry(root, width=40)
        self.topic_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(root, text="Mensagem:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.body_text = scrolledtext.ScrolledText(root, width=40, height=8)
        self.body_text.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        # Botões
        self.connect_btn = tk.Button(root, text="Conectar", command=self.connect_server)
        self.connect_btn.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        self.publish_btn = tk.Button(root, text="Publicar", command=self.publish_message, state=tk.DISABLED)
        self.publish_btn.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # Caixa de log
        self.log = scrolledtext.ScrolledText(root, width=60, height=12, state=tk.DISABLED)
        self.log.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.connected = False

    def log_message(self, msg):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def connect_server(self):
        if self.connected:
            messagebox.showinfo("Conexão", "Já conectado!")
            return
        # Aqui poderíamos testar uma requisição simples para validar a conexão
        try:
            r = requests.get(SERVER_URL + "/hello")
            if r.status_code == 200:
                self.connected = True
                self.log_message("Conectado ao servidor com sucesso!")
                self.publish_btn.config(state=tk.NORMAL)
            else:
                self.log_message(f"Falha ao conectar. Status: {r.status_code}")
        except Exception as e:
            self.log_message(f"Erro de conexão: {e}")

    def publish_message(self):
        if not self.connected:
            messagebox.showwarning("Aviso", "Conecte-se ao servidor primeiro!")
            return

        title = self.title_entry.get().strip()
        topic = self.topic_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()

        if not title or not topic or not body:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            payload = {"title": title, "topic": topic, "body": body}
            r = requests.post(SERVER_URL + "/publish", data=payload)
            if r.status_code == 200:
                self.log_message(f"Publicado no tópico '{topic}': {title}")
            else:
                self.log_message(f"Erro ao publicar ({r.status_code})")
        except Exception as e:
            self.log_message(f"Erro ao publicar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PublisherGUI(root)
    root.mainloop()
