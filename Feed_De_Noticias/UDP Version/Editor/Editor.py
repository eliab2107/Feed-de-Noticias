import socket
import json
import tkinter as tk
from tkinter import messagebox

# --- Configurações da Aplicação e Sockets ---
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
editor_socket = None

# --- Funções de Lógica do Editor ---
def connect_to_server():
   
    global editor_socket
    if editor_socket:
        messagebox.showinfo("Info", "Já está conectado ao servidor.")
        return

    try:
        editor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        editor_socket.connect((SERVER_HOST, SERVER_PORT))
        status_label.config(text="Status: Conectado ao servidor", fg="green")
        messagebox.showinfo("Sucesso", "Conectado ao servidor com sucesso!")
    except (ConnectionRefusedError, socket.gaierror):
        messagebox.showerror("Erro", "Não foi possível conectar ao servidor. Verifique se ele está online.")
        status_label.config(text="Status: Desconectado", fg="red")

def publish_message():
   
    global editor_socket
    if not editor_socket:
        messagebox.showerror("Erro", "Não conectado ao servidor.")
        return

    topic = topic_entry.get().strip()
    title = title_entry.get().strip()
    body = body_entry.get().strip()

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
        editor_socket.sendall(json.dumps(message).encode('utf-8'))
        messagebox.showinfo("Sucesso", f"Mensagem publicada com sucesso no tópico: '{topic}'")
        
        # Limpa os campos após a publicação
        topic_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        body_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao enviar a mensagem: {e}")

# --- Criação da Interface Gráfica (Tkinter) ---
root = tk.Tk()
root.title("Editor de Notícias")
root.geometry("400x350")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Status da conexão
status_label = tk.Label(main_frame, text="Status: Desconectado", fg="red", font=("Helvetica", 10, "bold"))
status_label.pack(pady=(0, 10))

# Campo de entrada para o tópico
tk.Label(main_frame, text="Tópico:", anchor='w').pack(fill=tk.X, pady=(0, 5))
topic_entry = tk.Entry(main_frame)
topic_entry.pack(fill=tk.X, ipady=3)

# Campo de entrada para o título
tk.Label(main_frame, text="Título:", anchor='w').pack(fill=tk.X, pady=(5, 5))
title_entry = tk.Entry(main_frame)
title_entry.pack(fill=tk.X, ipady=3)

# Campo de entrada para o resumo
tk.Label(main_frame, text="Resumo:", anchor='w').pack(fill=tk.X, pady=(5, 5))
body_entry = tk.Entry(main_frame)
body_entry.pack(fill=tk.X, ipady=3)

# Botões de ação
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=20)
publish_button = tk.Button(button_frame, text="Publicar", command=publish_message)
publish_button.pack(side=tk.LEFT, padx=5)

connect_button = tk.Button(main_frame, text="Conectar ao Servidor", command=connect_to_server)
connect_button.pack(pady=5)

# Executa o loop principal da interface
root.mainloop()