import sys
from controller.chatcontroller import ChatController
from controller.newChatController import NewChatController
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

app = QtWidgets.QApplication(sys.argv)
window = ChatController()
window.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)
window.show()
app.exec_()
