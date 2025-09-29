import socket
from threading import Thread
from Connection_manager import ConnectionManager


HOST = 'localhost'
CLIENT_PORT = 5000

def main():
    
    connection_manager = ConnectionManager()
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.bind((HOST, CLIENT_PORT))
    socket_client.listen(5)
    
    print(f"Servidor ouvindo em {HOST}:{CLIENT_PORT}")
    
    try:
        while True:
            client_socket, addr = socket_client.accept()
            print(f"[*] Aceitou conexão de {addr[0]}:{addr[1]}")
            
            client_thread = Thread(
                target=connection_manager.handle_client,
                args=(client_socket, addr)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[*] Servidor sendo desligado...")
    finally:
        socket_client.close()

if __name__ == "__main__":
    main()