from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from ruta import Ruta


class VentanaGeneradorNumeros(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("ventana_generador_numeros.ui"), self)
