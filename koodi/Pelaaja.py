

class Player():

    def __init__(self,nimi):
        self.nimi = nimi
        self.kasi = []
        self.qkasi = []
        self.pisteet = 0
        self.saadut_kortit = 0
        self.mokit = 0
        self.padat = 0
        self.assat =0
        self.pata2 = False
        self.ruutu10 = False
        self.pelattu = False #false jos ei ole vielä pelannut vuoroa
    def nollaaqkasi(self):
        self.qkasi = []
    def lisaaqkortti(self,kortti):
        self.qkasi.append(kortti)

    def poistaqkortti(self,kortti):
        if kortti in self.qkasi:
            self.qkasi.remove(kortti)
        else:
            print("debuggaus poista qkortti kasi")

    def getqkortit_kasi(self):
        return self.qkasi

    def lisaaassa(self):
        self.assat+=1

    def lisaapata(self):
        self.padat+=1

    def lisaapata2(self):
        self.pata2 = True

    def lisaaruutu10(self):
        self.ruutu10 = True

    def getpelattu(self):
        return self.pelattu

    def setpelattutrue(self):
        self.pelattu=True

    def setpelattufalse(self):
        self.pelattu = False

    def lisaa_kortti_kateen(self, kortti):
        self.kasi.append(kortti)

    def lisaa_kortti(self):
        self.saadut_kortit+=1

    def lisaa_mokki(self):
        self.mokit+=1

    def nollaa_mokit(self):
        self.mokit=0

    def get_kasi(self):
        return self.kasi

    def pelaa_kortti(self,kortti):

        self.kasi.remove(kortti)

    def return_name(self):
        return self.nimi