import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import http.client
import urllib.parse
import json

SERVER_HOST = 'localhost'
SERVER_PORT = 8080


class ClientApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cliente Feed de Notícias SSE")
        self.root.geometry("600x500")

        self.client_id = None 
        self.sse_thread = None
        self.stop_event = threading.Event()
        self.conn = None

        self.create_gui()
        self.root.mainloop()

    def create_gui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Tópico:").pack(anchor='w')
        self.topic_entry = tk.Entry(frame)
        self.topic_entry.pack(fill=tk.X)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Conectar", command=self.connect).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Inscrever", command=self.subscribe).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Desinscrever", command=self.unsubscribe).pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="Feed de Notícias:").pack(anchor='w', pady=(10, 0))
        self.feed_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
        self.feed_area.pack(fill=tk.BOTH, expand=True)

    def connect(self):
        if self.sse_thread and self.sse_thread.is_alive():
            messagebox.showinfo("Info", "Já conectado ao servidor")
            return

        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Atenção", "Digite um tópico inicial para conectar")
            return

        self.stop_event.clear()
        self.sse_thread = threading.Thread(target=self.listen_sse, args=(topic,), daemon=True)
        self.sse_thread.start()
        self.feed_area.insert(tk.END, f"Conectado ao servidor no tópico inicial '{topic}'\n")
        self.feed_area.see(tk.END)

    def subscribe(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Atenção", "Digite um tópico para se inscrever")
            return

        if not self.client_id:
            messagebox.showerror("Erro", "Conecte-se primeiro para obter um client_id")
            return

        body = {"action": "subscribe", "client_id": self.client_id, "topic": topic}
        self.send_put_request(body)
        self.feed_area.insert(tk.END, f"Pedido de inscrição enviado para '{topic}'\n")
        self.feed_area.see(tk.END)

    def unsubscribe(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Atenção", "Digite um tópico para se desinscrever")
            return

        if not self.client_id:
            messagebox.showerror("Erro", "Conecte-se primeiro para obter um client_id")
            return

        body = {"action": "unsubscribe", "client_id": self.client_id, "topic": topic}
        self.send_put_request(body)
        self.feed_area.insert(tk.END, f"Pedido de desinscrição enviado para '{topic}'\n")
        self.feed_area.see(tk.END)

    def send_put_request(self, body):
        try:
            conn = http.client.HTTPConnection(SERVER_HOST, SERVER_PORT, timeout=10)
            conn.request("PUT", "/", body=json.dumps(body), headers={"Content-Type": "application/json"})
            resp = conn.getresponse()
            conn.close()
            if resp.status != 200:
                messagebox.showerror("Erro", f"PUT falhou: {resp.status}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na requisição: {e}")

    def listen_sse(self, topic):
        try:
            conn = http.client.HTTPConnection(SERVER_HOST, SERVER_PORT, timeout=None)
            path = f"/stream?topic={urllib.parse.quote(topic)}"
            conn.request("GET", path, headers={"Accept": "text/event-stream"})
            resp = conn.getresponse()
            if resp.status != 200:
                self.root.after(0, lambda: self.feed_area.insert(tk.END, f"Falha ao conectar: {resp.status}\n"))
                return

            while not self.stop_event.is_set():
                line = resp.readline()
                if not line:
                    break
                line = line.decode('utf-8').strip()
                if line.startswith("data:"):
                    try:
                        data = json.loads(line[5:])
                        if "client_id" in data and not self.client_id:
                            self.client_id = data["client_id"]
                            self.root.after(0, lambda: self.feed_area.insert(tk.END, f"[INFO] Client ID: {self.client_id}\n"))
                        else:
                            self.root.after(0, self.update_feed, data)
                    except Exception:
                        continue

        except Exception as e:
            print(f"Erro SSE: {e}")

    def update_feed(self, data):
        self.feed_area.insert(tk.END, f" ==================== NEW NOTICE ====================\n"
                                      f"[TÓPICO]: {data.get('topic')}\n"
                                      f"[TÍTULO]: {data.get('title')}\n"
                                      f"[RESUMO]: {data.get('body')}\n\n")
        self.feed_area.see(tk.END)


if __name__ == "__main__":
    ClientApp()
