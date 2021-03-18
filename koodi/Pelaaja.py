

class Player():

    def __init__(self,nimi):
        self.nimi = nimi
        self.kasi = []
        self.pisteet = 0
        self.saadut_kortit = []
        self.mokit = 0

    def lisaa_kortti_kateen(self, kortti):
        self.kasi.append(kortti)

    def lisaa_kortti_saatuihin(self, kortti):
        self.saadut_kortit.append(kortti)

    def lisaa_mokki(self):
        self.mokit+=1

    def nollaa_mokit(self):
        self.mokit=0

    def get_kasi(self):
        return self.kasi

    def pelaa_kortti(self,i):
        kortti=self.kasi[i]
        self.kasi.remove(kortti)
        return kortti
    def return_name(self):
        return self.nimi