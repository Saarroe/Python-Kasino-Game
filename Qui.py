#Käyttöliittymä
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog
from pelikentta import Pelikentta
from Qui_add_player import Qui_addplayer
import sys
class GUI_aloitus(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.init_window()


    def get_player_amount(self):
        while 1:
            count, ok = QInputDialog.getText(self, "Amount of players (2-8)", "Enter amount:")
            try:
                count = int(count)
                break
            except ValueError:
                pass
        return count
    def start(self):
        # New game, how many players
        #count= self.get_player_amount()
        print("ok")


    def newplayer(self):
        text, ok = QInputDialog.getText(self, "Add new player",
                                        'Enter players name:')

        if ok:
            self.le.setText(str(text))

    def end(self):
        self.close()

    def adjust(self,widget):
        widget.adjustSize()


    def init_buttons(self):

        self.start_button = QPushButton("Start new game")
        self.start_button.clicked.connect(self.start())
        self.adjust(self.start_button)
        self.start_button.setStyleSheet("color: black; background: grey")
        self.horizontal.addWidget(self.start_button)

        self.load_button = QPushButton("Load game", self)
        self.load_button.setStyleSheet("color: black; background: grey")
       # self.load_button.clicked.connect(self.load_game())
        self.adjust(self.load_button)

        self.horizontal.addWidget(self.load_button)

        self.end_button = QPushButton("End game", self)
        self.end_button.setStyleSheet("color: black; background: grey")
        self.end_button.clicked.connect(self.end)
        self.adjust(self.end_button)
        self.horizontal.addWidget(self.end_button)


    def init_window(self):

        self.horizontal = QtWidgets.QHBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.horizontal)
        self.centralWidget().setLayout(self.vbox)
        self.setGeometry(500, 150, 1200, 800)
        self.setWindowTitle("Kasino")
        self.init_buttons()
        self.show()


    def load_game(self):
        pass


