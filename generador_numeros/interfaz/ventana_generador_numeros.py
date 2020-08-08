from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from soporte.ruta import Ruta


class VentanaGeneradorNumeros(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("ventana_generador_numeros.ui"), self)

	#Agrego validadores a los campos

	validador_decimales_1 = ValidadorDecimales(6, 2)
        validador_decimales_2 = ValidadorDecimales(10, 2)
	self.Txt_Semilla.setValidation(validador_decimales1)
	self.Txt_ConstanteA.setValidation(valida_decimales1)
	self.Txt_ConstanteC.setValidation(validador_decimales1)
	self.Txt_ConstanteM.setValidation(validador_decimales1)

	#Conecto los botones con los eventos

	self.Btn_generar_numeros.clicked.connect(self.generar_numeros)
	self.Btn_graficos.clicked.connect(self.generar_graficos)
	
	"""acciones"""
	
	# Accion generar numeros aleatorios

	def generar_numeros():


	# Accion generar graficos

	def generar_graficos():

	# Accion cargar los datos de la tabla

	def cargar_tabla():
