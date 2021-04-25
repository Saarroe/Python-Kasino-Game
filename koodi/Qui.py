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
        self.statusBar().setStyleSheet("Background: grey")
        self.statusBar().showMessage("Tervetuloa pelaamaan kasinoa")
        menubar = self.menuBar()
        menubar.setStyleSheet("Background: grey")
        self.fileMenu = menubar.addMenu('&Lopeta')
        self.fileMenu.heightForWidth(200)
        self.pisteMenu = menubar.addMenu('&Pistetaulukko')
        self.saveMenu = menubar.addMenu('&Tallenna peli')
        self.fileMenu.addAction(self.exitAct)

        self.timer = QtCore.QTimer()  #jotta ei tarvitse päivittää käyttöliittymää manuaalisesti
        self.timer.timeout.connect(lambda: self.updatequi())
        self.timer.start(15)


    def get_player_amount(self):
        while 1:
            self.dialog = QInputDialog()
            count, ok = self.dialog.getText(self,"Pelaaja","Pelaajien määrä\nAnna määrä väliltä (2-6):")

            try:
                count = int(count)
                if count < 2 or count >6:
                    pass
                else:
                    return count
            except ValueError:
                count, ok = QInputDialog.getText(self,"Pelaaja", "Väärä määrä pelaajia\nAnna luku väliltä (2-6):")

    def newplayer(self,x):


        text, ok = QInputDialog.getText(self, "Pelaaja", "Lisää uusi pelaaja\n{}. Pelaajan nimi:".format(x))
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
                QMessageBox.information(self, "Väärä nimi", "Pelaaja on jo pelissä\ntai\nPainoit cancel")


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

        self.vbox.addWidget(self.view)
        #luodaan siirtoja varten

        self.newbuttons()#pelin napit: seuraava vuoro, nayta kortit, talenna




        self.scene.addWidget(self.putcardbutton)
        self.scene.addWidget(self.takebutton)
        self.takebutton.move(500,200)

        pelaaja = self.peli.get_turn_pelaaja()
        teksti=pelaaja.return_name()

        self.nimi = QLabel(teksti)
        self.nimi.setStyleSheet("background-image: url(kuvat/board.jpg)")
        self.nimi.setFixedWidth(100)
        self.scene.addWidget(self.nimi)
        self.nimi.move(200,630)

        self.viiva = QtWidgets.QGraphicsLineItem()
        self.scene.addItem(self.viiva)

        self.setStyleSheet("Background: transparent")

        self.view.show()

    def newbuttons(self):

        self.putcardbutton = QPushButton("Laita kortti pöytään", self)  # sceneen napit laita pöytään
        self.putcardbutton.setStyleSheet("color: black; background: grey")
        self.putcardbutton.adjustSize()

        self.takebutton = QPushButton("Ota valitut kortit", self)
        self.takebutton.setStyleSheet("color: black; background: grey")
        self.takebutton.adjustSize()

        self.nextbutton = QPushButton("seuraava vuoro", self)
        self.nextbutton .setStyleSheet("color: black; background: grey")
        #self.nextbutton .clicked.connect(lambda: self.nextturn())
        self.nextbutton .adjustSize()

        self.showbutton = QPushButton("näyta kortit", self)
        self.showbutton.setStyleSheet("color: black; background: grey")
        self.showbutton.clicked.connect(lambda: self.showcards())
        self.showbutton.adjustSize()

        self.horizontal.addWidget(self.showbutton)
        self.horizontal.addWidget(self.putcardbutton)
        self.horizontal.addWidget(self.takebutton)
        self.horizontal.addWidget(self.nextbutton)
        self.vbox.addLayout(self.horizontal)  #lisätään horizontal view

    def showcards(self):  #avaa käden kortit
        x = 0
        kortit=self.peli.getqkortit_kasi()
        for kortti in kortit:
            kortti.avaakortti()
            self.scene.addWidget(kortti)
            kortti.move(-25+150*x,475)
            x += 1


    def updatequi(self):

        poytakortit = self.peli.get_poyta()
        qkortitpoyta = self.peli.getqkortit_poyta()
        qkortitkasi= self.peli.getqkortit_kasi()
        if len(poytakortit) == 0:
            pass
        else:
            x=0
            for kortti in poytakortit:
                if kortti.get_qui() == 1:
                    for qkortti in qkortitpoyta:
                        indeksi = qkortti.getindeksi()
                        if qkortti.getklikattu() == 0:
                            qkortti.move(-200+150*indeksi,75)
                        else:
                            qkortti.move(-200+150*indeksi,50)

                else:
                    kortti.set_quitrue()
                    self.kortti1 = Qui_card(kortti, self.peli,x)
                    self.kortti1.setTrue()
                    self.kortti1.avaakortti()
                    self.peli.lisaaqkorttipoyta(self.kortti1)
                    self.scene.addWidget(self.kortti1)
                    self.kortti1.move(-200+150*x,75)
                x+=1

            pelaaja = self.peli.get_turn_pelaaja()
            x=0
            for kortti in pelaaja.get_kasi():
                if kortti.get_qui() is True:

                    for qkortti in qkortitkasi:
                        indeksi = qkortti.getindeksi()
                        if qkortti.getklikattu() == 0:
                            qkortti.move(-25 + 150 * indeksi, 475)
                        else:
                            qkortti.move(-25+150*indeksi, 450)
                    break
                else:
                    kortti.set_quitrue()
                    self.kortti1 = Qui_card(kortti, self.peli, x)
                    self.kortti1.setFalse()
                    self.peli.lisaaqkortti(self.kortti1)
                    self.scene.addWidget(self.kortti1)
                    self.kortti1.move(-25+150*x,475)
                x+=1
            self.nimi.setText(pelaaja.return_name())
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
        self.setStyleSheet("background-image: url(kuvat/tausta.jpg)")
        self.show()

    def save_game(self):
        pass
    def load_game(self):
        pass



