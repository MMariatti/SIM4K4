import sys
from PyQt5.QtWidgets import QApplication
from interfaz.recursos import sim
from interfaz.ventana_montecarlo import VentanaMontecarlo


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VentanaMontecarlo()
    window.show()
    app.exec_()
