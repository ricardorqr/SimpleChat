import socket
import sys
import threading
import traceback


class NewServer:

    def __init__(self):
        self.SERVER_SOCKET = None
        self.clients = []
        self.HEADER = 1024
        self.PORT = 5555
        # self.SERVER = socket.gethostbyname(socket.gethostname())
        self.SERVER = ''
        self.ADDRESS = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT!"

    def start(self):
        self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_SOCKET.bind(self.ADDRESS)
        self.SERVER_SOCKET.listen()
        print('Server listening for clients...')

        while True:
            client = client_socket, (IP, PORT) = self.SERVER_SOCKET.accept()
            self.add_to_clients(client)
            print(f'Server {IP}: {PORT}')
            thread = threading.Thread(target=self.handle_client, args=(client_socket, (IP, PORT)))
            thread.start()
            print(f"Active connections: {threading.activeCount() - 1}")

    def handle_client(self, client_socket, client_address):
        print(f"Connected: {client_address}\n")
        while True:
            try:
                message_length = client_socket.recv(self.HEADER).decode(self.FORMAT)
                if message_length:
                    message_length = int(message_length)
                    message = client_socket.recv(message_length).decode(self.FORMAT)
                    if message == self.DISCONNECT_MESSAGE:
                        print(f"Disconnected: {client_address}")
                        break
                    self.broadcast_message_to_all_clients(client_socket, message)
            except Exception:
                print("1 - Exception in user code:")
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
                break
        client_socket.close()

    def broadcast_message_to_all_clients(self, client_socket, message):
        try:
            for client in self.clients:
                socket, (IP, PORT) = client
                if socket is not client_socket:
                        socket.sendall(message.encode(self.FORMAT))
        except Exception:
            print("1 - Exception in user code:")
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)
            self.clients.remove(client)
            socket.close()

    def add_to_clients(self, client):
        if client not in self.clients:
            self.clients.append(client)


if __name__ == '__main__':
    server = NewServer()
    server.start()
