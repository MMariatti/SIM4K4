from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from soporte.ruta import Ruta


class VentanaTomaDatos(QMainWindow):

    def __init__(self):

        # Genero ventana a partir de ui y creo controlador
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("interfaz/ventana_toma_datos.ui"), self)
