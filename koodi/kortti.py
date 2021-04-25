

class Kortti():
    Hertta = "Hertta"
    Ruutu = "Ruutu"
    Pata = "Pata"
    Risti = "Risti"
    def __init__(self, maa, arvo):
        self.set_maa(maa)
        self.arvo = arvo
        self.onkoqui = False




    def set_maa(self, maa):
        if maa in [Kortti.Ruutu, Kortti.Pata, Kortti.Risti, Kortti.Hertta]:
            self._maa = maa

    def get_maa(self):
        return self._maa

    def get_arvo(self):
        return self.arvo

    def set_quitrue(self): #joko true tai false
        self.onkoqui = True

    def get_qui(self):
        return self.onkoqui