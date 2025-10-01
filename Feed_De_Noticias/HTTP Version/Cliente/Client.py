import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import requests

SERVER_URL = "http://localhost:8080"

class SSEClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSE Client")

        tk.Label(root, text="Tópico:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.topic_entry = tk.Entry(root, width=30)
        self.topic_entry.grid(row=0, column=1, padx=5, pady=5)

        self.connect_btn = tk.Button(root, text="Conectar", command=self.connect_server)
        self.connect_btn.grid(row=0, column=2, padx=5, pady=5)

        self.subscribe_btn = tk.Button(root, text="Inscrever", command=self.subscribe_topic, state=tk.DISABLED)
        self.subscribe_btn.grid(row=1, column=1, padx=5, pady=5)

        self.unsubscribe_btn = tk.Button(root, text="Desinscrever", command=self.unsubscribe_topic, state=tk.DISABLED)
        self.unsubscribe_btn.grid(row=1, column=2, padx=5, pady=5)

        self.log = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
        self.log.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.running = False
        self.thread = None


    def log_message(self, msg):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)


    def connect_server(self):
        if self.running:
            messagebox.showinfo("Conexão", "Já conectado!")
            return

        self.running = True
        self.thread = threading.Thread(target=self.listen_stream, daemon=True)
        self.thread.start()

        self.log_message("Conectando ao servidor SSE...")
        self.subscribe_btn.config(state=tk.NORMAL)
        self.unsubscribe_btn.config(state=tk.NORMAL)


    def listen_stream(self):
        try:
            with requests.get(SERVER_URL + "/stream", stream=True) as response:
                if response.status_code != 200:
                    self.log_message(f"Erro: {response.status_code}")
                    return

                self.log_message("Conectado ao servidor SSE! Recebendo eventos...\n")

                for line in response.iter_lines(decode_unicode=True):
                    if not self.running:
                        break
                    if line and line.startswith("data:"):
                        data = line[5:].strip()
                        self.root.after(0, self.log_message, f"Evento: {data}")

        except Exception as e:
            self.root.after(0, self.log_message, f"Erro de conexão: {e}")


    def subscribe_topic(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Aviso", "Digite um tópico!")
            return
        try:
            r = requests.post(SERVER_URL + "/subscribe", data={"topic": topic})
            self.log_message(f"Inscrito no tópico '{topic}': {r.status_code}")
        except Exception as e:
            self.log_message(f"Erro ao inscrever: {e}")


    def unsubscribe_topic(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Aviso", "Digite um tópico!")
            return
        try:
            r = requests.post(SERVER_URL + "/unsubscribe", data={"topic": topic})
            self.log_message(f"Desinscrito do tópico '{topic}': {r.status_code}")
        except Exception as e:
            self.log_message(f"Erro ao desinscrever: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SSEClientGUI(root)
    root.mainloop()
