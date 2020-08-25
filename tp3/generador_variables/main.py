import sys
from PyQt5.QtWidgets import QApplication
from interfaz.recursos import sim
from interfaz.ventana_generador_varibles import VentanaGeneradorVariables


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VentanaGeneradorVariables()
    window.show()
    app.exec_()
