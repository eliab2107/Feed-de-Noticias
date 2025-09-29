import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- Configurações da Aplicação e Sockets ---
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
client_socket = None

# --- Funções de Lógica do Cliente ---
def connect_to_server():
    """Tenta conectar ao servidor e inicia as threads."""
    global client_socket
    if client_socket:
        messagebox.showinfo("Info", "Já está conectado ao servidor.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        status_label.config(text="Status: Conectado ao servidor", fg="green")
        
        # Inicia a thread para receber mensagens do servidor
        threading.Thread(target=receive_messages, daemon=True).start()
    except (ConnectionRefusedError, socket.gaierror):
        messagebox.showerror("Erro", "Não foi possível conectar ao servidor. Verifique se ele está online.")
        status_label.config(text="Status: Desconectado", fg="red")

def receive_messages():
    """Recebe mensagens do servidor e as exibe na caixa de texto."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                messagebox.showinfo("Info", "Conexão com o servidor foi encerrada.")
                break
            
            try:
                data = json.loads(message)
                topic = data.get('topic')
                title = data.get('title')
                body = data.get('body')
                feed_area.insert(tk.END, f" ==================== NEW NOTICE ====================\n[TÓPICO]: {topic}\n[TITULO]: {title}\n[RESUMO]: {body}\n\n")
                feed_area.see(tk.END) # Auto-scroll para a última mensagem
            except json.JSONDecodeError:
                feed_area.insert(tk.END, f"Mensagem recebida: {message}\n")

        except (ConnectionResetError, ConnectionAbortedError):
            status_label.config(text="Status: Conexão perdida", fg="red")
            break

def send_command(command):
    """Envia um comando de inscrição/cancelamento para o servidor."""
    global client_socket
    if not client_socket:
        messagebox.showerror("Erro", "Não conectado ao servidor.")
        return

    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showwarning("Atenção", "Por favor, digite um nome de tópico.")
        return

    message = {
        "command": command,
        "topic": topic
    }
    client_socket.sendall(json.dumps(message).encode('utf-8'))
    
    if command == "subscribe":
        messagebox.showinfo("Sucesso", f"Comando de inscrição para '{topic}' enviado.")
    else:
        messagebox.showinfo("Sucesso", f"Comando de cancelamento para '{topic}' enviado.")

# --- Criação da Interface Gráfica (Tkinter) ---
root = tk.Tk()
root.title("Cliente Feed de Notícias")
root.geometry("600x500")

# Frame principal
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Status da conexão
status_label = tk.Label(main_frame, text="Status: Desconectado", fg="red", font=("Helvetica", 10, "bold"))
status_label.pack(pady=(0, 10))

# Campo de entrada para o tópico
topic_frame = tk.Frame(main_frame)
topic_frame.pack(fill=tk.X, pady=5)
tk.Label(topic_frame, text="Tópico:").pack(side=tk.LEFT, padx=(0, 5))
topic_entry = tk.Entry(topic_frame, width=30)
topic_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# Botões de ação
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=5)
subscribe_button = tk.Button(button_frame, text="Inscrever", command=lambda: send_command("subscribe"))
subscribe_button.pack(side=tk.LEFT, padx=5)
unsubscribe_button = tk.Button(button_frame, text="Desinscrever", command=lambda: send_command("unsubscribe"))
unsubscribe_button.pack(side=tk.LEFT, padx=5)

# Botão de conexão
connect_button = tk.Button(main_frame, text="Conectar ao Servidor", command=connect_to_server)
connect_button.pack(pady=(10, 0))

# Área de exibição do feed
tk.Label(main_frame, text="Feed de Notícias:").pack(pady=(10, 0), anchor='w')
feed_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.NORMAL)
feed_area.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

# Executa o loop principal da interface
root.mainloop()