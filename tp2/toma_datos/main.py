import sys
from PyQt5.QtWidgets import QApplication
from interfaz.recursos import sim
from interfaz.ventana_toma_datos import VentanaTomaDatos


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VentanaTomaDatos()
    window.show()
    app.exec_()



