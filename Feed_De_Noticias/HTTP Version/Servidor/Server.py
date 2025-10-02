from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
import urllib.parse
import time
import queue
import uuid

HOST = 'localhost'
PORT = 8080

subscriptions = {}
clients = {}

subs_lock = threading.Lock()


class SSEHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        topic = urllib.parse.parse_qs(parsed.query).get('topic', [None])[0]
        if not topic:
            self.send_error(400, "Faltou parâmetro topic")
            return

       
        client_id = str(uuid.uuid4())
        q = queue.Queue()

        with subs_lock:
            clients[client_id] = {"queue": q, "topics": set([topic])}
            
            subscriptions.setdefault(topic, {})[client_id] = q
            print(f"[SERVER] Cliente {client_id} conectado em '{topic}'")

    
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.end_headers()

        self.wfile.write(f"data: {json.dumps({'client_id': client_id})}\n\n".encode("utf-8"))
        self.wfile.flush()

        try:
            while True:
                try:
                    msg = q.get(timeout=0.5)
                except queue.Empty:
                    continue

                try:
                    self.wfile.write(f"data: {json.dumps(msg)}\n\n".encode("utf-8"))
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    print(f"[SERVER] Cliente {client_id} desconectou")
                    break

        finally:
            with subs_lock:
                if client_id in clients:
                    for t in clients[client_id]["topics"]:
                        if client_id in subscriptions.get(t, {}):
                            del subscriptions[t][client_id]
                    del clients[client_id]
                    print(f"[SERVER] Cliente {client_id} removido")

    def do_POST(self):
        if self.path != "/publish":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)
        try:
            msg = json.loads(data.decode("utf-8"))
            topic = msg["topic"]
        except Exception as e:
            self.send_error(400, f"JSON inválido: {e}")
            return

        with subs_lock:
            queues = subscriptions.get(topic, {}).copy()
        for cid, q in queues.items():
            try:
                q.put(msg)
            except Exception as e:
                print(f"[SERVER] Erro ao enfileirar: {e}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK\n")

    def do_PUT(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)
        try:
            body = json.loads(data.decode("utf-8"))
            action = body.get("action")
            client_id = body.get("client_id")
            topic = body.get("topic")
        except Exception as e:
            self.send_error(400, f"JSON inválido: {e}")
            return

        if not action or not client_id or not topic:
            self.send_error(400, "Faltam parâmetros: action, client_id, topic")
            return

        with subs_lock:
            if client_id not in clients:
                self.send_error(404, "Cliente não encontrado")
                return

            if action == "subscribe":
                q = clients[client_id]["queue"]
                subscriptions.setdefault(topic, {})[client_id] = q
                clients[client_id]["topics"].add(topic)
                print(f"[SERVER] Cliente {client_id} SUBSCRIBED em '{topic}'")

            elif action == "unsubscribe":
                if client_id in subscriptions.get(topic, {}):
                    del subscriptions[topic][client_id]
                clients[client_id]["topics"].discard(topic)
                print(f"[SERVER] Cliente {client_id} UNSUBSCRIBED de '{topic}'")

            else:
                self.send_error(400, "Ação inválida (use 'subscribe' ou 'unsubscribe')")
                return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK\n")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), SSEHandler)
    print(f"[SERVER] Rodando em http://{HOST}:{PORT}")
    server.serve_forever()
