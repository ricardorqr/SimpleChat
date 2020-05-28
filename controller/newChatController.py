from PyQt5 import QtWidgets, uic
from common.util import Util
import socket
import threading

Ui_MainWindow, QtBaseClass = uic.loadUiType(Util.find_file("chatUI.ui"))


def pack_message(message):
    return message + '\n'


class NewChatController(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.user = ''
        self.data = ''

        self.HEADER = 64
        self.PORT = 5555
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT!"
        self.SERVER = "192.168.0.15"
        self.ADDRESS = (self.SERVER, self.PORT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDRESS)
        self.pushButtonSend.setEnabled(False)
        self.listening_message()

        self.pushButtonJoin.pressed.connect(self.join_chat)
        self.pushButtonSend.pressed.connect(self.send_message)

    def closeEvent(self, event):
        self.send_message_to_server(self.DISCONNECT_MESSAGE)
        event.accept()
        exit(0)

    def listening_message(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()

    def receive_message_from_server(self, socket):
        while True:
            buffer = socket.recv(1024)
            if not buffer:
                break
            message = buffer.decode(self.FORMAT)
            if message in 'joined':
                user = message.split(':')[1]
                message = user + " has joined"
                self.textEditChat.append(pack_message(message))
            else:
                self.textEditChat.append(pack_message(message))
        socket.close()

    def send_message(self):
        self.user = self.lineEdit.text().strip() + ": "
        self.data = self.textEditMessage.toPlainText().strip()
        message = self.user + self.data
        self.textEditChat.append(pack_message(message))
        self.textEditMessage.setText('')
        self.send_message_to_server(message)

    def join_chat(self):
        user = self.lineEdit.text()
        message = user + " has joined"
        self.pushButtonSend.setEnabled(True)
        self.lineEdit.setEnabled(False)
        self.pushButtonJoin.setEnabled(False)
        self.textEditChat.append(pack_message(message))
        self.send_message_to_server(message)

    def send_message_to_server(self, msg):
        message = msg.encode(self.FORMAT)
        message_length = len(message)
        send_length = str(message_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client_socket.send(send_length)
        self.client_socket.send(message)
