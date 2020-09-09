from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from soporte.ruta import Ruta


class VentanaMontecarlo(QMainWindow):

    """ Atributos """

    controlador = None

    """ Constructor """

    def __init__(self):

        # Genero ventana a partir de ui y creo controlador
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("interfaz/ventana_montecarlo.ui"), self)
