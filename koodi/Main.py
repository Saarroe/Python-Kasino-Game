from pelikentta import Pelikentta
from korttipakka import Korttipakka
import sys
from PyQt5.QtWidgets import QApplication
from Qui import GUI_aloitus
def main():


    global app  # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GUI_aloitus()

    sys.exit(app.exec_())
main()
