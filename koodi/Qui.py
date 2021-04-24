#Käyttöliittymä
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QMessageBox, QAction
from PyQt5.QtWidgets import QLabel
from pelikentta import Pelikentta
from Pelaaja import Player
from Qui_card import Qui_card
from Qui_board import Qui_board
from kortti import Kortti

class GUI_aloitus(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setCentralWidget(QtWidgets.QWidget())
        self._init_window()
        self.statusBar()  #luo statusbar jotta kerrotaan käyttäjälle tilanne
        self.peli = Pelikentta()  #luo kentän ja pakan
        self.exitAct = QAction('&Lopetetaan peli', self)
        self.exitAct.setStatusTip('Haluatko lopettaa pelin')
        self.exitAct.triggered.connect(self.close)
        self.statusBar()
        self.statusBar().showMessage("Tervetuloa pelaamaan kasinoa")
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&Lopeta')
        self.fileMenu.addAction(self.exitAct)


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
        text, ok = QInputDialog.getText(self, "Player", "Add new player\n{}. players name:".format(x))
        text= text.strip()
        if ok is False or len(text) == 0:
            return False

        elif len(self.peli.return_pelaajat()) > 0:
            for pelaaja in self.peli.return_pelaajat():
                if str(text) == pelaaja.return_name():
                    return False
        self.peli.lisaa_pelaaja(str(text))
        self.statusBar().showMessage("Pelaaja {} lisättiin onnistuneesti".format(text))
        return True

    def start(self):
        # New game, how many players
        count = self.get_player_amount()
        x = 0
        while x < count:
            ok = self.newplayer(x+1)
            if ok is True:
                x += 1
            else:
                QMessageBox.information(self, "Invalid name", "Player is already in the game\nor\nYou"
                                                              " clicked cancel")

        self.start_button.hide()  #Piilotetaan buttonit ja lisätään uusi näyttö
        self.load_button.hide()
        self.newGui()
        self.peli.aloita_peli()   # Pelaajat lisätty 2-8PLR, jaetaan kortit


        self.statusBar().showMessage("Peli alkaa jaetaan kortit")
        self.updatequi() #korttien lisäys kentälle, tilanteen päivtys

    def newGui(self):
        #luo scenen pelipöydän
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0,0,550,650)

        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setStyleSheet("background-image: url(kuvat/board.jpg); border: transparent")

        self.view.adjustSize()
        self.view.show()
        self.vbox.addWidget(self.view)
        #self.vbox.addStretch(0)

       #self.scene2 = QtWidgets.QGraphicsScene()
        #self.scene2.setSceneRect(500,500,200,200)
        #self.view2 = QtWidgets.QGraphicsView(self.scene, self)
        #self.view2.adjustSize()
        #self.view2.show()
        #self.vbox.addWidget(self.view2)

        self.newbuttons()  #pelin napit: seuraava vuoro, nayta kortit, talenna

    def newbuttons(self):

        self.nextbutton = QPushButton("seuraava vuoro", self)
        self.nextbutton .setStyleSheet("color: black; background: grey")
        #self.nextbutton .clicked.connect(lambda: self.nextturn())
        self.nextbutton .adjustSize()

        self.showbutton = QPushButton("nayta kortit", self)
        self.showbutton.setStyleSheet("color: black; background: grey")
        self.showbutton.clicked.connect(lambda: self.showcards())
        self.showbutton.adjustSize()

        self.save_button = QPushButton("Tallenna peli", self)
        self.save_button.setStyleSheet("color: black; background: grey")
        self.save_button.clicked.connect(lambda: self.save_game())
        self.save_button.adjustSize()

        self.horizontal.addWidget(self.nextbutton)
        self.horizontal.addWidget(self.showbutton)
        self.horizontal.addWidget(self.save_button)
        self.vbox.addLayout(self.horizontal)  #lisätään horizontal view

    def showcards(self):  #avaa käden kortit
        x = 0
        pelaaja = self.peli.get_turn_pelaaja()
        for kortti in pelaaja.get_kasi():
            self.kortti1 = Qui_card(kortti)
            self.kortti1.avaakortti()
            self.scene.addWidget(self.kortti1)
            self.kortti1.move(-25+150*x,475)
            x += 1




    def updatequi(self):


        poytakortit = self.peli.get_poyta()

        x=0
        for kortti in poytakortit:
            self.kortti1 = Qui_card(kortti)
            self.kortti1.avaakortti()
            self.scene.addWidget(self.kortti1)
            self.kortti1.move(-200+150*x,75)
            x+=1
        pelaaja = self.peli.get_turn_pelaaja()
        x=0
        for kortti in pelaaja.get_kasi():
            self.kortti1 = Qui_card(kortti)
            self.scene.addWidget(self.kortti1)
            self.kortti1.move(-25+150*x,475)
            x+=1
        self.view.show()
        self.statusBar().showMessage("Pelaajan {} vuoro".format(pelaaja.return_name()))


    def init_buttons(self):  #pelin alkunäyttö, jossa start ja load buttonit

        self.start_button = QPushButton("Start new game")
        self.start_button.clicked.connect(lambda: self.start())
        self.start_button.adjustSize()
        self.start_button.setStyleSheet("color: black; background: yellow")
        self.vbox.addWidget(self.start_button)

        self.load_button = QPushButton("Load game", self)
        self.load_button.setStyleSheet("color: black; background: yellow")
        self.load_button.clicked.connect(lambda: self.load_game())
        self.load_button.adjustSize()
        self.vbox.addWidget(self.load_button)

    def _init_window(self): #alkunäyttö


        self.horizontal = QtWidgets.QHBoxLayout()  #horizontal ja vertical layout
        self.vbox = QtWidgets.QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)
        self.setGeometry(500, 150, 1200, 800)
        self.setWindowTitle("Kasino")
        self.init_buttons()
        #self.setStyleSheet("background-image: url(kuvat/tausta.jpg)")
        self.show()

    def save_game(self):
        pass
    def load_game(self):
        pass



