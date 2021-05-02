from kortti import Kortti
import random
class Korttipakka():


    def __init__(self, x):  #x on true jos eka init
        self.kortit=[]
        self.eka = x

        self.set_kortit()

    def sekoita(self):
        random.shuffle(self.kortit)

    def getkortit(self):
        return self.kortit

    def lisaakortti(self, kortti):
        self.kortit.append(kortti)

    def set_kortit(self):  #luo uuden pakan 52 korttia ja sekoittaa sen
        maat = { "Hertta": Kortti.Hertta,"Ruutu": Kortti.Ruutu, "Pata": Kortti.Pata, "Risti": Kortti.Risti}
        if self.eka is True:
            for maa in maat:
                for arvo in range(2, 15):
                    kortti = Kortti(maat[maa], arvo)
                    self.kortit.append(kortti)
         #sekoita kortit
            self.sekoita()
        else:
            self.kortit = []

    def nosta_kortti(self):

       kortti=self.kortit.pop()

       return kortti


