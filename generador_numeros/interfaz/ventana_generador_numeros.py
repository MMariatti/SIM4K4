from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from dominio.controlador_generador_numeros import ControladorGeneradorNumeros
from soporte.validador_decimales import ValidadorDecimales
from soporte.validador_enteros import ValidadorEnteros
from soporte.ruta import Ruta


class VentanaGeneradorNumeros(QMainWindow):

	""" Atributos """

	controlador = None
	numeros_aleatorios = None

	""" Constructor """

	def __init__(self):
		# Genero ventana a partir de ui y creo controlador
		QMainWindow.__init__(self)
		uic.loadUi(Ruta.generar_ruta("interfaz/ventana_generador_numeros.ui"), self)
		self.controlador = ControladorGeneradorNumeros()

		# Agrego validadores a los campos
		validador_decimales = ValidadorDecimales(8, 4)
		validador_enteros = ValidadorEnteros(8)
		self.txt_semilla.setValidator(validador_decimales)
		self.txt_a.setValidator(validador_decimales)
		self.txt_c.setValidator(validador_decimales)
		self.txt_m.setValidator(validador_decimales)
		self.txt_cantidad_numeros.setValidator(validador_enteros)

		# Conecto los botones con los eventos
		self.cmb_metodo_generacion.currentIndexChanged.connect(self.accion_seleccionar_metodo)
		self.btn_limpiar_generar_numeros.clicked.connect(self.accion_limpiar_interfaz)
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

		# Obtengo metodo
		id_metodo = self.cmb_metodo_generacion.itemData(self.cmb_metodo_generacion.currentIndex())

		# Obtengo y valido parametros dependiendo del metodo
		semilla = self.txt_semilla.text()
		if semilla == "" or float(semilla) < 0:
			self.mostrar_mensaje_error("Error", "La semilla tiene que ser mayor o igual a cero")
			return
		a = self.txt_a.text()
		if a == "" or float(a) <= 0:
			self.mostrar_mensaje_error("Error", "La constante \"a\" tiene que ser mayor a cero")
			return
		c = None
		if id_metodo == 0:
			c = self.txt_c.text()
			if c == "" or float(c) <= 0:
				self.mostrar_mensaje_error("Error", "La constante \"c\" tiene que ser mayor a cero")
				return
		m = self.txt_m.text()
		if m == "" or float(m) <= 0:
			self.mostrar_mensaje_error("Error", "La constante \"m\" tiene que ser mayor a cero")
			return
		if float(semilla) >= float(m):
			self.mostrar_mensaje_error("Error", "La semilla tiene que ser menor a la constante \"m\"")
			return
		if float(a) >= float(m):
			self.mostrar_mensaje_error("Error", "La constante \"a\" tiene que ser menor a la constante \"m\"")
			return
		if c is not None and float(c) >= float(m):
			self.mostrar_mensaje_error("Error", "La constante \"c\" tiene que ser menor a la constante \"m\"")
			return
		cantidad_numeros = self.txt_cantidad_numeros.text()
		if cantidad_numeros == "" or int(cantidad_numeros) <= 0:
			self.mostrar_mensaje_error("Error", "La cantidad de números tiene que ser mayor a cero")
			return

		# Genero numeros aleatorios dependiendo del metodo seleccionado
		if id_metodo == 0:
			self.numeros_aleatorios = self.controlador.generador_congruente_mixo(cantidad_numeros, semilla, a, c, m)
		else:
			self.numeros_aleatorios = self.controlador.generador_congruente_multiplicativo(cantidad_numeros, semilla, a, m)

		# Cargo tabla
		self.cargar_tabla_numeros_aleatorios()

	def accion_prueba_frecuencia(self):
		pass

	""" Metodos """

	def preparar_interfaz(self):

		# Cargo combo box
		self.cmb_metodo_generacion.clear()
		self.cmb_metodo_generacion.addItem("Método congruente mixto", 0)
		self.cmb_metodo_generacion.addItem("Método congruente multiplicativo", 1)

		# Preparo tabla de numeros generados
		self.grid_numeros_generados.setColumnCount(4)
		self.grid_numeros_generados.setHorizontalHeaderLabels(["N° de orden", "Semilla", "Aleatorio", "A. Decimal"])

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

	def mostrar_mensaje_error(self, titulo, mensaje):

		# Muestro mensaje
		box = QMessageBox()
		box.setWindowTitle(titulo)
		box.setText(mensaje)
		box.setStandardButtons(QMessageBox.Ok)
		box.exec_()

	def cargar_tabla_numeros_aleatorios(self):

		self.grid_numeros_generados.setRowCount(len(self.numeros_aleatorios))
		index = 0
		for n in self.numeros_aleatorios:
			self.grid_numeros_generados.setItem(index, 0, QTableWidgetItem(str(n.get("nro_orden"))))
			self.grid_numeros_generados.setItem(index, 1, QTableWidgetItem(str(n.get("semilla")).replace(".", ",")))
			self.grid_numeros_generados.setItem(index, 2, QTableWidgetItem(str(n.get("aleatorio")).replace(".", ",")))
			self.grid_numeros_generados.setItem(index, 3, QTableWidgetItem(str(n.get("aleatorio_decimal"))
																		   .replace(".", ",")))
			index += 1

	""" Eventos """

	# Evento show
	def showEvent(self, QShowEvent):
		self.preparar_interfaz()
		self.limpiar_interfaz()
