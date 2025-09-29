import socket
import json
import tkinter as tk
from tkinter import messagebox



EDITOR_HOST = 'localhost'
EDITOR_PORT = 0

SERVER_HOST = 'localhost'
SERVER_PORT = 6000

class EditorApp():
    def __init__(self):
        self.editor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = (SERVER_HOST, SERVER_PORT)
        self.create_gui()

    def publish_message(self):

        topic = self.topic_entry.get().strip()
        title = self.title_entry.get().strip()
        body  = self.body_entry.get().strip()

        if not all([topic, title, body]):
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos: Tópico, Título e Resumo.")
            return
        
        message = {
            "command": "publish",
            "topic": topic,
            "title": title,
            "body": body
        }

        try:
            self.editor_socket.sendto(json.dumps(message).encode('utf-8'), self.server)
            messagebox.showinfo("Sucesso", f"Mensagem publicada com sucesso no tópico: '{topic}'")
            
            # Limpa os campos após a publicação
            self.topic_entry.delete(0, tk.END)
            self.title_entry.delete(0, tk.END)
            self.body_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao enviar a mensagem: {e}")

    # --- Criação da Interface Gráfica (Tkinter) ---
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Editor de Notícias")
        self.root.geometry("400x350")

        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Campo de entrada para o tópico
        tk.Label(main_frame, text="Tópico:", anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.topic_entry = tk.Entry(main_frame)
        self.topic_entry.pack(fill=tk.X, ipady=3)

        # Campo de entrada para o título
        tk.Label(main_frame, text="Título:", anchor='w').pack(fill=tk.X, pady=(5, 5))
        self.title_entry = tk.Entry(main_frame)
        self.title_entry.pack(fill=tk.X, ipady=3)

        # Campo de entrada para o resumo
        tk.Label(main_frame, text="Resumo:", anchor='w').pack(fill=tk.X, pady=(5, 5))
        self.body_entry = tk.Entry(main_frame)
        self.body_entry.pack(fill=tk.X, ipady=3)

        # Botões de ação
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        publish_button = tk.Button(button_frame, text="Publicar", command=self.publish_message)
        publish_button.pack(side=tk.LEFT, padx=5)

        # Executa o loop principal da interface
        self.root.mainloop()
        
if __name__ == "__main__":
    editor = EditorApp()