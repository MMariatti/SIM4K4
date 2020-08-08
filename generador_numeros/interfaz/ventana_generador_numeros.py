from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from dominio.controlador_generador_numeros import ControladorGeneradorNumeros
from soporte.validador_decimales import ValidadorDecimales
from soporte.ruta import Ruta


class VentanaGeneradorNumeros(QMainWindow):

	""" Atributos """

	controlador = None
	numeros_aleatorios = None

	""" Constructor """

	def __init__(self):
		# Genero ventana a partir de ui y creo controlador
		QMainWindow.__init__(self)
		uic.loadUi(Ruta.generar_ruta("ventana_generador_numeros.ui"), self)
		self.controlador = ControladorGeneradorNumeros()

		# Agrego validadores a los campos
		validador_decimales = ValidadorDecimales(10, 4)
		self.txt_semilla.setValidator(validador_decimales)
		self.txt_a.setValidator(validador_decimales)
		self.txt_c.setValidator(validador_decimales)
		self.txt_m.setValidator(validador_decimales)

		# Conecto los botones con los eventos
		self.cmb_metodo_generacion.currentIndexChanged.connect(self.accion_seleccionar_metodo)
		self.btn_limpiar.clicked.connect(self.accion_limpiar_interfaz)
		self.btn_generar_numeros.clicked.connect(self.accion_generar_numeros)
		self.btn_prueba_frecuencia.clicked.connect(self.accion_prueba_frecuencia)

	""" Acciones """

	def accion_seleccionar_metodo(self):

		# Activo o desactivo input de constante c dependiendo del metodo elegido
		id_metodo = self.cmb_metodo_generacion.itemData(self.cmb_metodo_generacion.currentIndex())
		if id_metodo == 0:
			self.txt_c.setEnabled(True)
		else:
			self.txt_c.clear()
			self.txt_c.setEnabled(False)

	def accion_limpiar_interfaz(self):

		# Llamo a metodo limpiar interfaz
		self.limpiar_interfaz()

	def accion_generar_numeros(self):
		pass

	def accion_prueba_frecuencia(self):
		pass

	""" Metodos """

	def preparar_interfaz(self):

		# Cargo combo box
		self.cmb_metodo_generacion.clear()
		self.cmb_metodo_generacion.addItem("Método congruente mixto", 0)
		self.cmb_metodo_generacion.addItem("Método congruente multiplicativo", 1)

		# Preparo tabla de numeros generados
		self.grid_numeros_generados.setColumnCount(3)
		self.grid_numeros_generados.setHorizontalHeaderLabels(["N° de orden", "Semilla", "Número aleatorio"])

	def limpiar_interfaz(self):

		# Limpio txts
		self.txt_semilla.clear()
		self.txt_a.clear()
		self.txt_c.clear()
		self.txt_m.clear()
		self.txt_cantidad_numeros.clear()

		# Selecciono opcion por defecto en combo boxs
		self.cmb_metodo_generacion.setCurrentIndex(0)

		# Limpio grilla
		self.grid_numeros_generados.clearSelection()
		self.grid_numeros_generados.setCurrentCell(-1, -1)
		self.grid_numeros_generados.setRowCount(0)

	def cargar_tabla_numeros_aleatorios(self):
		pass

	""" Eventos """

	# Evento show
	def showEvent(self, QShowEvent):
		self.preparar_interfaz()
		self.limpiar_interfaz()
