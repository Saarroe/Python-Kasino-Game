from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication)

class Qui_addplayer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.dialog_button = QPushButton("Add new player")
        self.dialog_button.clicked.connect(self.newplayer)
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle("New player")
        self.show()

    def newplayer(self):
        text,ok = QInputDialog.getText(self, "Add new player",
                                        'Enter players name:')

        if ok:
            self.le.setText(str(text))

