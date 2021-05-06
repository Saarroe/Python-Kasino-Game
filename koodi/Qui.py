#Käyttöliittymä
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QMessageBox, QAction
from PyQt5.QtWidgets import QLabel
from pelikentta import Pelikentta
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from Pelaaja import Player
from Qui_card import Qui_card
from Qui_pisteet import Qui_pisteet
from kortti import Kortti

class GUI_aloitus(QMainWindow):

    def __init__(self):
        super().__init__()
        self.peli = None
        self.setCentralWidget(QtWidgets.QWidget())
        self._init_window()
        self.statusBar()  #luo statusbar jotta kerrotaan käyttäjälle tilanne

        self.exitAct = QAction('&Lopetetaan peli', self)
        self.exitAct.triggered.connect(self.close)

        self.statusBar()
        self.statusBar().setStyleSheet("Background: orange")
        self.statusBar().showMessage("Tervetuloa pelaamaan kasinoa")

        menubar = self.menuBar()
        menubar.setStyleSheet("Background: orange")

        self.fileMenu = menubar.addMenu('&Lopeta')
        self.pisteMenu = menubar.addMenu('&Pistetaulukko')
        self.saveMenu = menubar.addMenu('&Tallenna peli')
        self.musiikki = menubar.addMenu('&Musiikki')

        self.fileMenu.addAction(self.exitAct)

        self.pisteet = QAction('&Näytä pistetilanne', self)  #Tilanne viimeksi pelatun kokonaisen kierroksen jälkeen
        self.pisteet.triggered.connect(lambda: self.pistetaulukko())
        self.pisteMenu.addAction(self.pisteet)

        self.tallennus = QAction('&Tallennetaan peli')
        self.tallennus.triggered.connect(lambda: self.save_game())
        self.saveMenu.addAction(self.tallennus)

#Musiikin teko
        self.sound = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile("musiikki/bensound-sunny.mp3")))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.sound.setPlaylist(self.playlist)
        self.sound.play()
        self.sound.setMuted(True)

        self.music = QAction('&Musiikki')
        self.music.setCheckable(True)
        self.music.setChecked(False)
        self.music.triggered.connect(lambda: self.setmusic())
        self.musiikki.addAction(self.music)

    def setmusic(self):  #Asettaa musiikin päälle tai pois
        if self.sound.isMuted():
            self.sound.setMuted(False)

        else:
            self.sound.setMuted(True)

    def pistetaulukko(self):
        if self.peli != None:
            self.piste = Qui_pisteet(self.peli, False)

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
                QMessageBox.information(self, "Väärä luku", "Anna luku väliltä 2-6")

    def newplayer(self,x):

        text, ok = QInputDialog.getText(self, "Pelaaja", "Lisää uusi pelaaja\n{}. Pelaajan nimi:".format(x))
        text= text.strip()
        if ok is False or len(text) == 0:
            return False

        elif len(self.peli.return_pelaajat()) > 0:
            for pelaaja in self.peli.return_pelaajat():
                if str(text) == pelaaja.return_name():
                    return False
        if text[0] == '#':
            return False
        if len(text)>10:

            text = text[0:15]
        self.peli.lisaa_pelaaja(str(text))
        self.statusBar().showMessage("Pelaaja {} lisättiin onnistuneesti".format(text))
        return True

    def start(self):
        self.peli = Pelikentta(True)  # luo kentän ja pakan, on eka init pakalle
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
        pelaajat = self.peli.return_pelaajat()
        pelaajat[0].setjakajatrue()


        self.updatequi()# Pelaajat lisätty 2-8PLR, jaetaan kortit

        self.timer = QtCore.QTimer()  # jotta ei tarvitse päivittää käyttöliittymää klikkauksille
        self.timer.timeout.connect(lambda: self.timerklikkaus())
        self.timer.start(100)

        self.statusBar().showMessage("Peli alkaa jaetaan kortit")
        self.updatequi() #korttien lisäys kentälle, tilanteen päivtys

    def newGui(self):
        #luo scenen pelipöydän
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0,0,650,750)

        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setStyleSheet("background-image: url(kuvat/board.jpg)")

        self.vbox.addWidget(self.view)
        #luodaan siirtoja varten

        self.newbuttons()#pelin napit: seuraava vuoro, nayta kortit, talenna




        self.scene.addWidget(self.putcardbutton)
        self.scene.addWidget(self.takebutton)
        self.takebutton.move(500,200)

        pelaaja = self.peli.get_turn_pelaaja()
        teksti=pelaaja.return_name()

        self.nimi = QLabel(teksti)

        self.nimi.setStyleSheet("background: green")
        self.nimi.setFixedWidth(200)
        self.nimi.setFixedHeight(30)
        self.nimi.setAlignment(QtCore.Qt.AlignCenter)
        self.nimi.setFont(QtGui.QFont("Arial", 15))
        self.scene.addWidget(self.nimi)
        self.nimi.move(160,670)

        self.viiva = QLabel()
        self.scene.addWidget(self.viiva)
        self.viiva.setStyleSheet("background: black")
        self.viiva.setFixedHeight(5)
        self.viiva.setFixedWidth(1150)
        self.viiva.move(-250, 230)

        self.pakkakuva = QLabel()
        kuva = QtGui.QPixmap("kuvat/purple_back.jpg")
        self.pakkakuva.setPixmap(kuva.scaled(100,150))
        self.scene.addWidget(self.pakkakuva)
        self.pakkakuva.move(650,260)


        self.pakkalaskuri= QLabel()
        self.scene.addWidget(self.pakkalaskuri)
        self.pakkalaskuri.move(650,425)
        self.pakkalaskuri.setStyleSheet("background: green")
        self.pakkalaskuri.setFixedWidth(100)
        self.pakkalaskuri.setFixedHeight(30)

        self.setStyleSheet("background: green")

        self.pakkalaskuri.setAlignment(QtCore.Qt.AlignCenter)
        self.view.show()

    def newbuttons(self):

        self.putcardbutton = QPushButton("Laita kortti pöytään", self)  # sceneen napit laita pöytään
        self.putcardbutton.setStyleSheet("color: black; background: orange")
        self.putcardbutton.clicked.connect(lambda: self.putcard())
        self.putcardbutton.adjustSize()

        self.takebutton = QPushButton("Ota valitut kortit", self)
        self.takebutton.setStyleSheet("color: black; background: orange")
        self.takebutton.clicked.connect(lambda: self.takecard())
        self.takebutton.adjustSize()

        self.nextbutton = QPushButton("Seuraava vuoro", self)
        self.nextbutton.setStyleSheet("color: black; background: orange")
        self.nextbutton.clicked.connect(lambda: self.nextturn())
        self.nextbutton.adjustSize()

        self.showbutton = QPushButton("Näyta kortit", self)
        self.showbutton.setStyleSheet("color: black; background: orange")
        self.showbutton.clicked.connect(lambda: self.showcards())
        self.showbutton.adjustSize()

        self.horizontal.addWidget(self.showbutton)
        self.horizontal.addWidget(self.putcardbutton)
        self.horizontal.addWidget(self.takebutton)
        self.horizontal.addWidget(self.nextbutton)
        self.vbox.addLayout(self.horizontal)  #lisätään horizontal view

        self.uusikierros = None

    def nextturn(self):

        self.timer.stop()
        ekapelaaja = self.peli.get_turn_pelaaja()

        if ekapelaaja.getpelattu() is True:

            for qkortti in self.peli.getqkortit_poyta():
                qkortti.setklikattu0()
            for qkortti in ekapelaaja.getqkortit_kasi():#piilottaa kädessä olevat kortit

                qkortti.suljekortti()
                qkortti.hide()

            ekapelaaja.setpelattufalse()
            self.peli.seuraava_vuoro()
            pelaaja = self.peli.get_turn_pelaaja()

            if len(pelaaja.get_kasi())>0:
                for qkortti in pelaaja.getqkortit_kasi():
                    qkortti.show()
                self.statusBar().showMessage("Pelaajan {} vuoro alkaa".format(pelaaja.return_name()))
                self.updatequi()

                self.timer.start()

            else:
                QMessageBox.information(self, "Kierros loppui", "Näytetään pistetilanne")
                for pelaaja in self.peli.return_pelaajat():  #Annetaan pöydässä olevat loput kortit pelaajalle

                    #joka otta kortteja pöydästä viimeksi
                    if pelaaja.getvika() is True:
                        for kortti in self.peli.get_poyta():
                            pelaaja.lisaa_kortti()
                            if kortti.get_arvo() == 14:
                                pelaaja.lisaaassa()
                            if kortti.get_arvo() == 2 and kortti.get_maa() == "Pata":
                                pelaaja.lisaapata2()
                            if kortti.get_arvo() == 10 and kortti.get_maa() == "Ruutu":
                                pelaaja.lisaaruutu10()
                            if kortti.get_maa() == "Pata":
                                pelaaja.lisaapata()

                        break
                for qkortti in self.peli.getqkortit_poyta():
                    qkortti.clear()  # poistaa kortin ja pistää sen läpinäkyväks
                    qkortti.setpixmapnone()
                    qkortti.move(700, 500)

                self.peli.laskepisteet()

                suurin =0
                for pelaaja in self.peli.return_pelaajat():
                    if pelaaja.getpisteet() > suurin:
                        suurin = pelaaja.getpisteet()
                self.pistetaul = Qui_pisteet(self.peli,True)

                if suurin > 15:

                    self.pakkalaskuri.hide()
                    self.nextbutton.hide()
                    self.showbutton.hide()
                    self.takebutton.hide()
                    self.putcardbutton.hide()
                    self.nimi.hide()
                    self.viiva.hide()

                    uusi = QLabel("  Peli päättyi\n  Onnea voittajalle!")

                    uusi.setFont(QtGui.QFont("Times", 30))

                    self.view.setStyleSheet("background-image: url(kuvat/voitto.jpg)")

                    self.scene.addWidget(uusi)

                else:
                    if self.uusikierros is None:
                        self.uusikierros = QPushButton("Aloita uusi kierros", self)
                        self.uusikierros.setStyleSheet("color: black; background: orange")
                        self.uusikierros.clicked.connect(lambda: self.nollaa_kaikki())
                        self.vbox.addWidget(self.uusikierros)
                    else:
                        self.uusikierros.show()


        else:
            self.statusBar().showMessage("Tee ensiksi siirto: Ota halutut kortit tai laita kortti pöytään")
            self.timer.start()

    def nollaa_kaikki(self):  #Nollaa kaiken kierroksen loputtua, ennen uuden alkua, ja asettaa turnin oikein

        self.uusikierros.hide()

        self.peli.nollaapelitiedot()  #Peli tietojen nollaus
        x=0

        for pelaaja in self.peli.return_pelaajat(): #Pelaajien tietojen lopetus
            if pelaaja.getjakaja() is True:
                pelaaja.setjakajafalse()
                turn = x
            pelaaja.nollaatiedot()
            x+=1

        pelaajat=self.peli.return_pelaajat()
        pelaajat[turn+1].setjakajatrue()

        self.peli.nollaapelitiedot()
        self.peli.asetavuoro(turn+1)  #asettaa seuraavan pelaajan jakajaksi

        self.peli.nollaakorttiqui() # luodaan siten täysin uudet quicardit

        self.peli.aloita_peli()
        self.pakkakuva.show()
        self.updatequi()
        self.timer.start()
    def takecard(self):

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
                    for pelaaja1 in self.peli.return_pelaajat():
                        pelaaja1.setvikafalse()
                    pelaaja.setvikatrue()

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

                    self.peli.lisaakorttipelaajalle()
                    if kasiq.getkortti().get_arvo() == 14:
                        pelaaja.lisaaassa()
                    if kasiq.getkortti().get_arvo() == 2 and kasiq.getkortti().get_maa() == "Pata":
                        pelaaja.lisaapata2()
                    if kasiq.getkortti().get_arvo() == 10 and kasiq.getkortti().get_maa() == "Ruutu":
                        pelaaja.lisaaruutu10()
                    if kasiq.getkortti().get_maa() == "Pata":

                        pelaaja.lisaapata()
                    if len(self.peli.getqkortit_poyta()) == 0:
                        pelaaja.lisaa_mokki()
                    kasiq.clear()
                    kasiq.setpixmapnone()
                    kasiq.move(700, 500)
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
        if pelaaja.getpelattu() is False:
            if len(self.peli.getqkortit_poyta())>9:
                QMessageBox.warning(self, "Pöytä täynnä", "Pöytä täynnä, et pelaa fiksusti")
            else:
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
                qkortti.move(-250 + 125 * y, 75)
            else:
                qkortti.move(-250 + 125 * y, 50)
            y += 1
        x=0
        for qkortti1 in qkortitkasi:
            if qkortti1.getklikattu() == 0:
                qkortti1.move(-25 + 150 * x, 490)
            else:
                qkortti1.move(-25 + 150 * x, 465)
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
                kortti1.move(-300 + 125 * x, 75)
            x+=1
        ####################### pöytä
        if len(kasikortit) == 0 :  #peli loppuu

            pass
        elif len(qkortitkasi) == 0:  #ei luotoja qui card olioita, eka alustus
            x=0
            for kortti in kasikortit:
                kortti.set_quitrue()
                qkortti1 = Qui_card(kortti, self.peli)
                pelaaja.lisaaqkortti(qkortti1)
                self.scene.addWidget(qkortti1)
                qkortti1.move(-25 + 150 * x, 490)
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
                    qkortti1.move(-25 + 150 * x, 490)
                x+=1
            x=0
            for qkortti in qkortitkasi:
                qkortti.move(-25 + 150 * x, 490)
        self.nimi.setText(pelaaja.return_name())
        if len(self.peli.pakka.getkortit()) > 0:
            self.pakkalaskuri.show()
            self.pakkalaskuri.setText("kortit: {}".format(str(len(self.peli.pakka.getkortit()))))
            self.pakkalaskuri.adjustSize()
        else:
            self.pakkalaskuri.setText("Pakka loppui")
            self.pakkakuva.hide()
        self.view.show()



    def init_buttons(self):  #pelin alkunäyttö, jossa start ja load buttonit

        self.start_button = QPushButton("Aloita uusi peli")
        self.start_button.clicked.connect(lambda: self.start())

        self.start_button.setStyleSheet("color: black; background: transparent; border-radius: 15px solid black;"
                                        "font-size: 36px")
        self.start_button.setFixedHeight(120)
        self.start_button.setFixedWidth(250)
        self.start_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.vbox.addWidget(self.start_button)



        self.load_button = QPushButton("Lataa peli", self)
        self.load_button.setStyleSheet("color: black; background: transparent; border-radius: 15px solid black; "
                                       "font-size: 36px")
        self.load_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_button.clicked.connect(lambda: self.load_game())
        self.load_button.setFixedHeight(120)
        self.load_button.setFixedWidth(250)
        self.horizontal.addWidget(self.load_button)
        self.vbox.addWidget(self.load_button)


    def _init_window(self): #alkunäyttö


        self.horizontal = QtWidgets.QHBoxLayout()  #horizontal ja vertical layout
        self.vbox = QtWidgets.QVBoxLayout()
        self.centralWidget().setLayout(self.vbox)
        self.setGeometry(0, 0, 1300, 900)
        self.setWindowTitle("Kasino")
        self.init_buttons()
        self.setStyleSheet("background-image: url(kuvat/tausta2.jpg)")
        self.show()

    def save_game(self):  #tallentaa pelin tiedot
        if self.peli == None:
            QMessageBox.warning(self, "Ei pelaajia", "Aloita peli ensin")
        else:
            text, ok = QInputDialog.getText(self, "Tallennus", "Anna tallennus tiedoston nimi:")
            teksti = text.strip()
            if ok is True and len(teksti) >0:
                tiedosto = open("{}.txt".format(teksti), "w")
                tiedosto.write("#pelaajat pelissa:\n")
                for pelaaja in self.peli.return_pelaajat():  #pelaajien nimet
                    nimi=pelaaja.return_name()
                    tiedosto.write(nimi)
                    tiedosto.write("\n")
                tiedosto.write("#kortit pakassa:\n")
                pakka = self.peli.get_pakka()
                for kortti in pakka.getkortit():
                    tiedosto.write("{} {}\n".format(kortti.get_maa(), kortti.get_arvo()))
                tiedosto.write("#kortit poydalla:\n") #kortit pöydällä
                for kortti in self.peli.get_poyta():
                    tiedosto.write("{} {}\n".format(kortti.get_maa(), kortti.get_arvo()))
                tiedosto.write("#pelin tiedot:\n")
                tiedosto.write("{}\n".format(self.peli.get_vuoro()))
                tiedosto.write("#pelaajien tiedot\n")
                for pelaaja in self.peli.return_pelaajat():  #kaikkien pelaajien tiedot
                    tiedosto.write("# {} {}\n".format(pelaaja.return_name(), len(pelaaja.get_kasi())))
                    for kortti in pelaaja.get_kasi():  #pelaajan x kortit kädessä
                        tiedosto.write("{} {}\n".format(kortti.get_maa(), kortti.get_arvo()))
                    tiedosto.write("{}\n".format(pelaaja.getpisteet())) #pisteet
                    tiedosto.write("{}\n".format(pelaaja.getjakaja())) #onko jakaja
                    tiedosto.write("{}\n".format(pelaaja.getkortit())) #saadut kortit
                    tiedosto.write("{}\n".format(pelaaja.getassat())) #saadut assat
                    tiedosto.write("{}\n".format(pelaaja.getpadat())) #saadut padat
                    tiedosto.write("{}\n".format(pelaaja.getmokit())) #saadut mokit
                    tiedosto.write("{} pata2\n".format(pelaaja.getpata2())) #onko pata2
                    tiedosto.write("{} ruutu10\n".format(pelaaja.getruutu10())) #onko ruutu10
                    tiedosto.write("{} onko vuoro päättynyt\n".format(pelaaja.getpelattu()))  #onko vuoro päättynyt
                    tiedosto.write("{} onko saanut kortteja viimeksi\n".format(pelaaja.getvika()))
                    #onko saanut vikana kortteja

                tiedosto.close()
                QMessageBox.information(self, "Tallennus", "Peli tallennettu tiedostoon {}.txt".format(teksti))

            else:
                QMessageBox.information(self, "Tallennus", "Tallennus tiedoston nimi ei kelpaa\ntai painoit cancel")


    def load_game(self):
        text, ok = QInputDialog.getText(self, "Lataaminen", "Anna ladattavan tiedoston nimi:")

        if ok is True:
            teksti = text.strip()
            try:  #onko peli olemassa
                tekst="{}.txt".format(teksti)
                tiedosto = open(tekst, "r")  #avaa tiedoston
                rivi = tiedosto.readline()  #ekana turha rivi

                self.peli = Pelikentta(False) #luo uuden pelin minne lisätään pelaajat, pakka aluksi tyhjä
                while len(rivi)>0:
                    rivi = rivi.strip()
                    if rivi == "#pelaajat pelissa:":
                        rivi = tiedosto.readline()
                        while rivi[0] != '#' and len(rivi)>0:  #ekana pelaajat pelissä
                            nimi = rivi.strip()
                            self.peli.lisaa_pelaaja(nimi)

                            rivi = tiedosto.readline()
                    elif rivi == "#kortit pakassa:":  #lisätään kortit pakkaan
                        maat = {"Hertta": Kortti.Hertta, "Ruutu": Kortti.Ruutu, "Pata": Kortti.Pata,
                                "Risti": Kortti.Risti}
                        rivi = tiedosto.readline()

                        while rivi[0] != '#':
                            maa, arvo2 = rivi.split(" ")
                            maa=maa.strip()
                            arvo2 = arvo2.strip()
                            arvo = int(arvo2)
                            kortti = Kortti(maat[maa], arvo)

                            self.peli.pakka.lisaakortti(kortti)
                            rivi = tiedosto.readline()

                    elif rivi == "#kortit poydalla:":  #lisätään kortit pöytään

                        rivi = tiedosto.readline()
                        while rivi[0] != '#':
                            maa, arvo2 = rivi.split(" ")
                            maa = maa.strip()
                            arvo2 = arvo2.strip()
                            arvo = int(arvo2)
                            kortti = Kortti(maat[maa], arvo)
                            self.peli.lisaa_kortti_poytaan(kortti)
                            rivi = tiedosto.readline()

                    elif rivi == "#pelin tiedot:":
                        rivi = tiedosto.readline()
                        vuoro = rivi.strip()
                        self.peli.asetavuoro(int(vuoro))

                        rivi = tiedosto.readline()
                    elif rivi == "#pelaajien tiedot":
                        rivi = tiedosto.readline()
                        for pelaaja in self.peli.return_pelaajat():
                            turha,nimi,kortit = rivi.split(" ")
                            kortit = kortit.strip()
                            kortit = int(kortit)
                            if nimi.strip() == pelaaja.return_name():  #vain varmistus että oikein
                                rivi = tiedosto.readline()

                                x=0
                                while x<kortit:

                                    maa, arvo2 = rivi.split(" ")
                                    maa = maa.strip()
                                    arvo2 = arvo2.strip()
                                    arvo = int(arvo2)
                                    kortti = Kortti(maat[maa], arvo)
                                    pelaaja.lisaa_kortti_kateen(kortti)
                                    rivi = tiedosto.readline()
                                    x+=1


                                pisteet = rivi.strip()
                                pisteet = int(pisteet)
                                pelaaja.lisaapisteet(pisteet) #pisteet

                                rivi = tiedosto.readline()  # onko jakaja
                                jakaja = rivi.strip()
                                if jakaja == "True":
                                    pelaaja.setjakajatrue()


                                rivi = tiedosto.readline() #saadut kortit
                                rivi = rivi.strip()
                                saakortit = int(rivi)
                                pelaaja.lisaakortit(saakortit)

                                rivi = tiedosto.readline() #saadut assat
                                rivi = rivi.strip()
                                assat = int(rivi)
                                pelaaja.lisaaassat(assat)

                                rivi = tiedosto.readline()  # saadut padat
                                rivi = rivi.strip()
                                padat = int(rivi)
                                pelaaja.lisaapadat(padat)

                                rivi = tiedosto.readline()  # saadut mokit
                                rivi = rivi.strip()
                                mokit = int(rivi)
                                pelaaja.lisaamokit(mokit)
                                rivi = tiedosto.readline()  # onko pata2
                                rivi = rivi.split(" ")
                                rivi[0] = rivi[0].strip()
                                if rivi[0] == "True":
                                    pelaaja.lisaapata2()
                                rivi = tiedosto.readline()  # onko ruutu10
                                rivi = rivi.split(" ")
                                rivi[0] = rivi[0].strip()
                                if rivi[0] == "True":
                                    pelaaja.lisaaruutu10()
                                rivi = tiedosto.readline()# onko pelattu true
                                rivi = rivi.split(" ")
                                rivi[0] = rivi[0].strip()
                                if rivi[0] == "True":

                                    pelaaja.setpelattutrue()
                                rivi = tiedosto.readline()  # onko vika true
                                rivi = rivi.split(" ")
                                rivi[0] = rivi[0].strip()
                                if rivi[0] == "True":

                                    pelaaja.setvikatrue()
                                rivi = tiedosto.readline()
                            else:  #ei pitäisi ikinä mennä, debuggaus
                                print("Nyt jotain pahasti pielessä")

                self.start_button.hide()  # Piilotetaan buttonit ja lisätään uusi näyttö
                self.load_button.hide()
                self.newGui()
                self.updatequi()
                self.timer = QtCore.QTimer()  # jotta ei tarvitse päivittää käyttöliittymää klikkauksille
                self.timer.timeout.connect(lambda: self.timerklikkaus())
                self.timer.start(100)

            except OSError:  #ei tiedostoa
                QMessageBox.warning(self, "Väärä tiedosto", "Tiedoston nimellä {}.txt \n ei löytynyt tallennettua"
                                                            "peliä".format(teksti))
        else:
            QMessageBox.information(self, "Cancel", "Suljit lataa peli ikkunan")






