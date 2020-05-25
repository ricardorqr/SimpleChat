from PyQt5 import QtWidgets, uic
from common.util import Util
import socket
import threading

Ui_MainWindow, QtBaseClass = uic.loadUiType(Util.find_file("chatUI.ui"))


def pack_message(message):
    return message + '\n'


class ChatController(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.__user = ''
        self.__data = ''
        self.__IP = '192.168.0.16'
        self.__PORT = 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.__IP, self.__PORT))
        self.thread = None
        self.pushButtonSend.setEnabled(False)
        self.listening_message()

        self.pushButtonJoin.pressed.connect(self.join_chat)
        self.pushButtonSend.pressed.connect(self.send_message)

    def closeEvent(self, event):
        self.thread.close()
        self.client_socket.close()
        event.accept()

    def listening_message(self):
        self.thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        self.thread.start()

    def receive_message_from_server(self, socket):
        while True:
            buffer = socket.recv(1024)
            if not buffer:
                break
            message = buffer.decode('utf-8')
            if message in 'joined':
                user = message.split(':')[1]
                message = user + " has joined"
                self.textEditChat.append(pack_message(message))
            else:
                self.textEditChat.append(pack_message(message))
        socket.close()

    def send_message(self):
        self.__user = self.lineEdit.text().strip() + ": "
        self.__data = self.textEditMessage.toPlainText().strip()
        message = self.__user + self.__data
        self.textEditChat.append(pack_message(message))
        self.textEditMessage.setText('')
        self.client_socket.send(message.encode('utf-8'))

    def join_chat(self):
        user = self.lineEdit.text()
        message = user + " has joined"
        self.pushButtonSend.setEnabled(True)
        self.textEditChat.append(pack_message(message))
        self.lineEdit.setEnabled(False)
        self.pushButtonJoin.setEnabled(False)
        self.client_socket.send(("joined: " + user).encode('utf-8'))
