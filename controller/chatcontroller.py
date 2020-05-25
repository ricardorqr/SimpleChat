from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from common.util import Util
import socket
import threading

Ui_MainWindow, QtBaseClass = uic.loadUiType(Util.find_file("chatUI.ui"))


class ChatController(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.user = ''
        self.data = ''
        self.IP = '192.168.0.16'
        self.PORT = 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP, self.PORT))
        self.listen_message_in_a_thread()

        self.pushButtonJoin.pressed.connect(self.join_chat)
        self.pushButtonSend.pressed.connect(self.send_message)

    def listen_message_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()

    def receive_message_from_server(self, socket):
        while True:
            buffer = socket.recv(1024)
            if not buffer:
                break
            message = buffer.decode('utf-8')
            print(message)
            if message in 'joined':
                user = message.split(':')[1]
                message = user + " has joined"
                self.textEditChat.append(message + '\n')
            else:
                self.textEditChat.append(message + '\n')
        socket.close()

    def send_message(self):
        self.user = self.lineEdit.text().strip() + ": "
        self.data = self.textEditMessage.toPlainText().strip()
        message = self.user + self.data
        self.textEditChat.append(message + '\n')
        self.client_socket.send(message.encode('utf-8'))

    def join_chat(self):
        user = self.lineEdit.text()
        message = user + " has joined"
        print(message)
        self.textEditChat.append(message + '\n')
        self.lineEdit.setEnabled(False)
        self.pushButtonJoin.setEnabled(False)
        self.client_socket.send(("joined: " + user).encode('utf-8'))
