import socket
import threading


class Server:

    def __init__(self):
        self.server_socket = None
        self.IP = ''
        self.PORT = 5555
        self.clients = []
        self.last_message = ''
        self.create_server()

    def create_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        print('Listening for clients...')
        self.server_socket.listen()
        self.receive_message_in_a_thread()

    def receive_message(self, socket):
        while True:
            incoming_message = socket.recv(1024)
            if not incoming_message:
                break
            self.last_message = incoming_message.decode('utf-8')
            self.broadcast_message_to_all_clients(socket)
        socket.close()

    def broadcast_message_to_all_clients(self, sender_sockets):
        for client in self.clients:
            socket, (IP, PORT) = client
            if socket is not sender_sockets:
                socket.sendall(self.last_message.encode('utf-8'))

    def receive_message_in_a_thread(self):
        while True:
            client = so, (IP, PORT) = self.server_socket.accept()
            self.add_to_clients(client)
            print(f'Connected to {IP}: {PORT}')
            thread = threading.Thread(target=self.receive_message, args=(so,))
            thread.start()

    def add_to_clients(self, client):
        if client not in self.clients:
            self.clients.append(client)


if __name__ == '__main__':
    Server()
