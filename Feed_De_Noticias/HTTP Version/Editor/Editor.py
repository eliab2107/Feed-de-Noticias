import tkinter as tk
from tkinter import messagebox
import json
import urllib.request

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

class EditorApp:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Editor de Notícias SSE")
        self.root.geometry("400x350")
        self.create_gui()
        self.root.mainloop()

    def create_gui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Tópico:").pack(anchor='w')
        self.topic_entry = tk.Entry(frame)
        self.topic_entry.pack(fill=tk.X)

        tk.Label(frame, text="Título:").pack(anchor='w')
        self.title_entry = tk.Entry(frame)
        self.title_entry.pack(fill=tk.X)

        tk.Label(frame, text="Resumo:").pack(anchor='w')
        self.body_entry = tk.Entry(frame)
        self.body_entry.pack(fill=tk.X)

        tk.Button(frame, text="Publicar", command=self.publish).pack(pady=10)

    def publish(self):
        topic = self.topic_entry.get().strip()
        title = self.title_entry.get().strip()
        body = self.body_entry.get().strip()
        if not all([topic, title, body]):
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        data = {"topic": topic, "title": title, "body": body}
        req = urllib.request.Request(
            f"http://{SERVER_HOST}:{SERVER_PORT}/publish",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                messagebox.showinfo("Sucesso", f"Mensagem publicada no tópico '{topic}'")
                self.topic_entry.delete(0, tk.END)
                self.title_entry.delete(0, tk.END)
                self.body_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao publicar: {e}")

if __name__ == "__main__":
    print("Iniciando Editor...")
    EditorApp()
