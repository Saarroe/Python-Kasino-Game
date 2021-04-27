#Käyttöliittymä
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QMessageBox, QAction
from PyQt5.QtWidgets import QLabel
from pelikentta import Pelikentta
from Pelaaja import Player
from Qui_card import Qui_card
from Qui_pisteet import Qui_pisteet
from kortti import Kortti

class GUI_aloitus(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setCentralWidget(QtWidgets.QWidget())
        self._init_window()
        self.statusBar()  #luo statusbar jotta kerrotaan käyttäjälle tilanne
        self.peli = Pelikentta()  #luo kentän ja pakan
        self.exitAct = QAction('&Lopetetaan peli', self)
        self.exitAct.triggered.connect(self.close)

        self.statusBar()
        self.statusBar().setStyleSheet("Background: grey")
        self.statusBar().showMessage("Tervetuloa pelaamaan kasinoa")

        menubar = self.menuBar()
        menubar.setStyleSheet("Background: grey")

        self.fileMenu = menubar.addMenu('&Lopeta')
        self.pisteMenu = menubar.addMenu('&Pistetaulukko')
        self.saveMenu = menubar.addMenu('&Tallenna peli')

        self.fileMenu.addAction(self.exitAct)

        self.pisteet = QAction('&Näytä pistetilanne', self)  #Tilanne viimeksi pelatun kokonaisen kierroksen jälkeen
        self.pisteet.triggered.connect(lambda: self.pistetaulukko())
        self.pisteMenu.addAction(self.pisteet)



    def pistetaulukko(self):
        if len(self.peli.return_pelaajat()) > 0:

            self.piste = Qui_pisteet(self.peli)

        else:
            QMessageBox.warning(self, "Ei pelaajia", "Aloita peli ensin")

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
        self.peli.aloita_peli()

        self.updatequi()# Pelaajat lisätty 2-8PLR, jaetaan kortit

        self.timer = QtCore.QTimer()  # jotta ei tarvitse päivittää käyttöliittymää klikkauksille
        self.timer.timeout.connect(lambda: self.timerklikkaus())
        self.timer.start(100)

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
        self.nimi.setFixedWidth(175)
        self.nimi.setFixedHeight(25)
        self.scene.addWidget(self.nimi)
        self.nimi.move(160,630)

       # self.viiva = QtWidgets.QGraphicsLineItem()
        #self.scene.addItem(self.viiva)
        self.pakkakuva = QLabel()
        kuva = QtGui.QPixmap("kuvat/purple_back.jpg")
        self.pakkakuva.setPixmap(kuva.scaled(100,150))
        self.scene.addWidget(self.pakkakuva)
        self.pakkakuva.move(650,250)


        self.pakkalaskuri= QLabel()
        self.scene.addWidget(self.pakkalaskuri)
        self.pakkalaskuri.move(650,400)
        self.pakkalaskuri.setStyleSheet("background-image: url(kuvat/board.jpg)")
        self.pakkalaskuri.setFixedWidth(100)
        self.pakkalaskuri.setFixedHeight(30)
        #self.setStyleSheet("Background: transparent")
        self.setStyleSheet("background: green")

        self.view.show()

    def newbuttons(self):

        self.putcardbutton = QPushButton("Laita kortti pöytään", self)  # sceneen napit laita pöytään
        self.putcardbutton.setStyleSheet("color: black; background: grey")
        self.putcardbutton.clicked.connect(lambda: self.putcard())
        self.putcardbutton.adjustSize()

        self.takebutton = QPushButton("Ota valitut kortit", self)
        self.takebutton.setStyleSheet("color: black; background: grey")
        self.takebutton.clicked.connect(lambda: self.takecard())
        self.takebutton.adjustSize()

        self.nextbutton = QPushButton("Seuraava vuoro", self)
        self.nextbutton .setStyleSheet("color: black; background: grey")
        self.nextbutton .clicked.connect(lambda: self.nextturn())
        self.nextbutton .adjustSize()

        self.showbutton = QPushButton("Näyta kortit", self)
        self.showbutton.setStyleSheet("color: black; background: grey")
        self.showbutton.clicked.connect(lambda: self.showcards())
        self.showbutton.adjustSize()

        self.horizontal.addWidget(self.showbutton)
        self.horizontal.addWidget(self.putcardbutton)
        self.horizontal.addWidget(self.takebutton)
        self.horizontal.addWidget(self.nextbutton)
        self.vbox.addLayout(self.horizontal)  #lisätään horizontal view

    def nextturn(self):
        self.timer.stop()
        ekapelaaja = self.peli.get_turn_pelaaja()

        if ekapelaaja.getpelattu() is True and len(ekapelaaja.getqkortit_kasi()) >0:

            for qkortti in self.peli.getqkortit_poyta():
                qkortti.setklikattu0()
            for qkortti in ekapelaaja.getqkortit_kasi():#piilottaa kädessä olevat kortit

                qkortti.suljekortti()
                qkortti.hide()
            print("kortit: {} {}".format(ekapelaaja.return_name(), ekapelaaja.getkortit()))
            print("assat: {} {}".format(ekapelaaja.return_name(), ekapelaaja.getassat()))
            print("padat: {} {}".format(ekapelaaja.return_name(), ekapelaaja.getpadat()))
            print("mökit: {} {}".format(ekapelaaja.return_name(), ekapelaaja.getmokit()))
            ekapelaaja.setpelattufalse()
            self.peli.seuraava_vuoro()

            pelaaja = self.peli.get_turn_pelaaja()
            for qkortti in pelaaja.getqkortit_kasi():
                qkortti.show()
            self.statusBar().showMessage("Pelaajan {} vuoro alkaa".format(pelaaja.return_name()))
            self.updatequi()

        else:
            self.statusBar().showMessage("Tee ensiksi siirto: Ota halutut kortit tai laita kortti pöytään")
        self.timer.start()
    def takecard(self):  #Käy läpi uusiksi rauhassa

        vara = []
        quip = []

        pelaaja = self.peli.get_turn_pelaaja()
        if pelaaja.getpelattu() is False and len(pelaaja.getqkortit_kasi()) > 0:
            kasiq = None
            for qkortti in pelaaja.getqkortit_kasi():
                if qkortti.getklikattu() == 1:
                    kasiq = qkortti

            for qkortti in self.peli.getqkortit_poyta():
                if qkortti.getklikattu() == 1:
                    uusi = qkortti.getkortti()
                    vara.append(uusi)
                    quip.append(qkortti)

            if len(vara)>0 and kasiq is not None:
                kasi = kasiq.getkortti()
                ok = self.peli.laske_oikein(vara,kasi)

                if ok is False:
                    self.statusBar().showMessage("Siirto ei ole sääntöjen mukainen")
                else:
                    self.statusBar().showMessage("Pelaajan {} siirto tehty, "
                                                 "paina seuraava vuoro".format(pelaaja.return_name()))
                    for qkortti in quip:
                        qkortti.setklikattu0()
                        kortti = qkortti.getkortti()
                        self.peli.otakortti_poydasta(kortti)

                        self.peli.poistaqkorttipoyta(qkortti)
                        qkortti.clear()  #poistaa kortin ja pistää sen läpinäkyväks
                        qkortti.setpixmapnone()
                        qkortti.move(700,500)
                        pelaaja.lisaa_kortti()

                        if kortti.get_arvo() == 14:
                            pelaaja.lisaaassa()
                        if kortti.get_arvo() == 2 and kortti.get_maa() == "Pata":
                            pelaaja.lisaapata2()
                        if kortti.get_arvo() == 10 and kortti.get_maa() == "Ruutu":
                            pelaaja.lisaaruutu10()
                        if kortti.get_maa() == "Pata":
                            pelaaja.lisaapata()


                    kasiq.setklikattu0()
                    pelaaja.poistaqkortti(kasiq)
                    pelaaja.pelaa_kortti(kasiq.getkortti())
                    pelaaja.lisaa_kortti()
                    kasiq.clear()
                    kasiq.setpixmapnone()
                    kasiq.move(700, 500)

                    self.peli.lisaakorttipelaajalle()
                    if kortti.get_arvo() == 14:
                        pelaaja.lisaaassa()
                    if kortti.get_arvo() == 2 and kortti.get_maa() == "Pata":
                        pelaaja.lisaapata2()
                    if kortti.get_arvo() == 10 and kortti.get_maa() == "Ruutu":
                        pelaaja.lisaaruutu10()
                    if kortti.get_maa()=="Pata":
                        pelaaja.lisaapata()
                    if len(self.peli.getqkortit_poyta()) == 0:
                        pelaaja.lisaa_mokki()



                    pelaaja.setpelattutrue()
            else:
                self.statusBar().showMessage("Valitse yksi kortti kädestä ja halutut kortit pöydältä")
        else:
            self.statusBar().showMessage("Pelaajan {} siirto tehty, "
                                           "paina seuraava vuoro".format(pelaaja.return_name()))
        self.updatequi()

    def putcard(self):
        x=0

        pelaaja = self.peli.get_turn_pelaaja()
        if pelaaja.getpelattu() is False and len(pelaaja.getqkortit_kasi()) >0:
            for qkortti in pelaaja.getqkortit_kasi():
                if qkortti.getklikattu() == 1:
                    kortti = qkortti.getkortti()
                    qkortti.setklikattu0()
                    self.peli.lisaaqkorttipoyta(qkortti)
                    pelaaja.poistaqkortti(qkortti)
                    self.peli.pelaa_kortin_poytaan(kortti)
                    pelaaja.setpelattutrue()
                    x=0
                    self.statusBar().showMessage("Pelaajan {} siirto tehty".format(pelaaja.return_name()))
                    break
                else:
                    x=1

        else:
            self.statusBar().showMessage("Pelaajan {} vuoro päättynyt, "
                                         "paina seuraava vuoro".format(pelaaja.return_name()))
        if x==1:
            self.statusBar().showMessage("Klikkaa ensiksi kädestä korttia minkä haluat valita")
        self.updatequi()


    def showcards(self):  #avaa käden kortit
        x = 0
        pelaaja = self.peli.get_turn_pelaaja()
        if pelaaja.getpelattu() is False and len(pelaaja.getqkortit_kasi()) > 0:
            kortit=pelaaja.getqkortit_kasi()
            for kortti in kortit:
                kortti.avaakortti()
                self.scene.addWidget(kortti)
                kortti.move(-25+150*x,460)
                x += 1
            self.updatequi()
        else:
            self.statusBar().showMessage("Vuorosi päättyi jo")

    def timerklikkaus(self):
        y=0
        pelaaja = self.peli.get_turn_pelaaja()
        qkortitpoyta = self.peli.getqkortit_poyta()
        qkortitkasi = pelaaja.getqkortit_kasi()
        for qkortti in qkortitpoyta:
            if qkortti.getklikattu() == 0:
                qkortti.move(-200 + 150 * y, 75)
            else:
                qkortti.move(-200 + 150 * y, 50)
            y += 1
        x=0
        for qkortti1 in qkortitkasi:
            if qkortti1.getklikattu() == 0:
                qkortti1.move(-25 + 150 * x, 460)
            else:
                qkortti1.move(-25 + 150 * x, 435)
            x+=1
        self.view.show()

    def updatequi(self):

        pelaaja = self.peli.get_turn_pelaaja()
        poytakortit = self.peli.get_poyta()
        kasikortit = pelaaja.get_kasi()
        qkortitpoyta = self.peli.getqkortit_poyta()
        qkortitkasi= pelaaja.getqkortit_kasi()
#Pöytäkortit kun kerran luotu niin aina auki, vain klikkaus muuttuu, minkä tekee timeri

        if len(qkortitpoyta) == 0 and len(poytakortit)>0:  #ei luotuja kortteja pöydässä
            x=0
            for kortti in poytakortit:
                kortti.set_quitrue()
                kortti1 = Qui_card(kortti, self.peli)
                kortti1.avaakortti()
                self.peli.lisaaqkorttipoyta(kortti1)
                self.scene.addWidget(kortti1)
                kortti1.move(-200 + 150 * x, 75)
            x+=1
        ####################### pöytä
        if len(kasikortit) == 0:  #peli loppuu
            print("Peli loppui")
            self.loppu = Qui_pisteet()
        elif len(qkortitkasi) == 0:  #ei luotoja qui card olioita, eka alustus
            x=0
            for kortti in kasikortit:
                kortti.set_quitrue()
                qkortti1 = Qui_card(kortti, self.peli)
                pelaaja.lisaaqkortti(qkortti1)
                self.scene.addWidget(qkortti1)
                qkortti1.move(-25 + 150 * x, 460)
                x+=1
        else:
            x=0
            for kortti in kasikortit:
                if kortti.get_qui() is True:
                    pass
                else:
                    kortti.set_quitrue()
                    qkortti1 = Qui_card(kortti, self.peli)
                    qkortti1.avaakortti()
                    pelaaja.lisaaqkortti(qkortti1)
                    self.scene.addWidget(qkortti1)
                    qkortti1.move(-25 + 150 * x, 460)
                x+=1
            x=0
            for qkortti in qkortitkasi:
                qkortti.move(-25 + 150 * x, 460)
        self.nimi.setText(pelaaja.return_name())
        if len(self.peli.pakka.getkortit()) > 0:
            self.pakkalaskuri.setText("kortit: {}".format(str(len(self.peli.pakka.getkortit()))))
            self.pakkalaskuri.adjustSize()
        else:
            self.pakkalaskuri.setText("Pakka loppui")
            self.pakkakuva.hide()
        self.view.show()



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
        self.setGeometry(0, 0, 1300, 900)
        self.setWindowTitle("Kasino")
        self.init_buttons()
        #self.setStyleSheet("background-image: url(kuvat/tausta.jpg)")
        self.show()

    def save_game(self):
        pass
    def load_game(self):
        pass



