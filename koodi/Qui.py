#Käyttöliittymä
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QMessageBox, QListWidgetItem, QListWidget
from PyQt5.QtWidgets import QLabel
from pelikentta import Pelikentta
from Pelaaja import Player
from Qui_card import Qui_card
from Qui_board import Qui_board

class GUI_aloitus(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.init_window()
        self.peli = Pelikentta()
        self.Qui_kortit = Qui_card()

        #self.make_board()
    def make_board(self):

        self.boardlist = Qui_board()


    def get_player_amount(self):
        while 1:
            count, ok = QInputDialog.getText(self,"Players", "Amount of players (2-8)\nEnter amount:")

            try:
                count = int(count)
                if count < 2 or count >8:
                    pass
                else:
                    return count
            except ValueError:
                count, ok = QInputDialog.getText(self,"Players", "Wrong Amount of players (2-8)\nEnter new amount:")


    def newplayer(self,x):

        eka = "Add New player"
        toka = "Players name:"
        text, ok = QInputDialog.getText(self, "Player",  "Add new player\n{}. players name:".format(x))
        text= text.strip()
        if ok == False or len(text) == 0 :
            return False

        elif len(self.peli.return_pelaajat()) > 0:
            for pelaaja in self.peli.return_pelaajat():
                if str(text) == pelaaja.return_name():
                    return False
        self.peli.lisaa_pelaaja(str(text))
        return True

    def start(self):
        # New game, how many players
        count = self.get_player_amount()
        x=0
        while x < count:
            ok = self.newplayer(x+1)
            if ok == True:
                x+=1
            else:
                QMessageBox.information(self, "Invalid name", "Player is already in the game\nor\nYou"
                                                              " clicked cancel")
        # Pelaajat lisätty 2-8PLR, jaetaan kortit
        self.peli.aloita_peli()
        #luo pöytä ja esitä kortit:


    def board(self):
        for kortti in self.peli.get_poyta(): #haetaan Qui_card olio
            kortti.set_visibility(True)
            qui_card = self.Qui_kortit.get_auki(kortti)

            self.list.addItem(qui_card)
            print("ok")
        self.update_list()


    def save_game(self):
        pass

    def ubdate_list(self,list):
        self.listview = QtWidgets.QListView(self.list)
        self.listview.show()



    def init_buttons(self):

        self.start_button = QPushButton("Start new game")
        self.start_button.clicked.connect(lambda: self.start())
        self.start_button.adjustSize
        self.start_button.setStyleSheet("color: black; background: grey")
        self.horizontal.addWidget(self.start_button)

        self.load_button = QPushButton("Load game", self)
        self.load_button.setStyleSheet("color: black; background: grey")
        self.load_button.clicked.connect(lambda: self.load_game())
        self.load_button.adjustSize()
        self.horizontal.addWidget(self.load_button)

        self.save_button = QPushButton("Save game", self)
        self.save_button.setStyleSheet("color: black; background: grey")
        self.save_button.clicked.connect(lambda: self.save_game())
        self.save_button.adjustSize()
        self.horizontal.addWidget(self.save_button)

        self.end_button = QPushButton("End game", self)
        self.end_button.setStyleSheet("color: black; background: grey")
        self.end_button.clicked.connect(self.close)
        self.end_button.adjustSize()
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
        self.boardlist = Qui_board()

        self.boardlist.setStyleSheet("{background-image: url(board.jpg);}")
        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.boardlist)

       # self.view = QtWidgets.QListView(self.boardlist)
       # self.view.adjustSize()
      #  self.view.show()
      #  self.centralWidget().



    def load_game(self):
        pass



