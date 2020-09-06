from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from dominio.controlador_generador_variables import ControladorGeneradorVariables
from soporte.validador_decimales import ValidadorDecimales
from soporte.validador_enteros import ValidadorEnteros
from soporte.ruta import Ruta


class VentanaGeneradorVariables(QMainWindow):

	""" Atributos """

	controlador = None
	variables_aleatorias = []
	tipo_distribucion = None
	mu = None
	sigma = None
	lambd = None

	""" Constructor """

	def __init__(self):

		# Genero ventana a partir de ui y creo controlador
		QMainWindow.__init__(self)
		uic.loadUi(Ruta.generar_ruta("interfaz/ventana_generador_variables.ui"), self)
		self.controlador = ControladorGeneradorVariables()

		# Agrego validadores a los campos
		validador_decimales_negativos = ValidadorDecimales(negative=True)
		validador_decimales = ValidadorDecimales()
		validador_enteros = ValidadorEnteros(12)
		self.txt_mu.setValidator(validador_decimales_negativos)
		self.txt_sigma.setValidator(validador_decimales)
		self.txt_lambda.setValidator(validador_decimales)
		self.txt_cantidad_variables.setValidator(validador_enteros)
		self.txt_cantidad_intervalos.setValidator(validador_enteros)

		# Conecto los botones con los eventos
		self.cmb_tipo_distribucion.currentIndexChanged.connect(self.accion_seleccionar_tipo_distribucion)
		self.btn_limpiar_generar_variables.clicked.connect(self.accion_limpiar_interfaz_generar_variables)
		self.btn_generar_variables.clicked.connect(self.accion_generar_variables)
		self.btn_limpiar_prueba_frecuencia.clicked.connect(self.accion_limpiar_interfaz_prueba_frecuencia)
		self.btn_generar_grafico.clicked.connect(self.accion_generar_grafico)
		self.btn_test_chi_cuadrado.clicked.connect(self.accion_test_chi_cuadrado)

	""" Acciones """

	def accion_seleccionar_tipo_distribucion(self):

		# Activo o desactivo inputs dependiendo del tipo de distribucion elegido
		id_tipo_distribucion = self.cmb_tipo_distribucion.itemData(self.cmb_tipo_distribucion.currentIndex())
		if id_tipo_distribucion == 0:
			self.txt_mu.setEnabled(True)
			self.txt_sigma.setEnabled(True)
			self.txt_lambda.clear()
			self.txt_lambda.setEnabled(False)
		else:
			self.txt_mu.clear()
			self.txt_mu.setEnabled(False)
			self.txt_sigma.clear()
			self.txt_sigma.setEnabled(False)
			self.txt_lambda.setEnabled(True)

	def accion_limpiar_interfaz_generar_variables(self):

		# Limpio lista de variables aleatorias
		self.variables_aleatorias = []

		# Llamo a metodo limpiar interfaz de generar variables
		self.limpiar_interfaz_generar_variables()

	def accion_generar_variables(self):

		# Obtengo tipo de distribucion
		id_tipo_distribucion = self.cmb_tipo_distribucion.itemData(self.cmb_tipo_distribucion.currentIndex())

		# Obtengo y valido parametros dependiendo del metodo
		mu = None
		sigma = None
		lambd = None
		if id_tipo_distribucion == 0:
			mu = self.txt_mu.text()
			if mu == "":
				self.mostrar_mensaje("Error", "La constante \"mu\" no puede ser vacía")
				return
			sigma = self.txt_sigma.text()
			if sigma == "" or float(sigma.replace(",", ".")) < 0:
				self.mostrar_mensaje("Error", "La constante \"sigma\" tiene que ser mayor o igual a cero")
				return
		else:
			lambd = self.txt_lambda.text()
			if lambd == "" or float(lambd.replace(",", ".")) <= 0:
				self.mostrar_mensaje("Error", "La constante \"lambda\" tiene que ser mayor a cero")
				return
		cantidad_numeros = self.txt_cantidad_variables.text()
		if cantidad_numeros == "" or int(cantidad_numeros) <= 0:
			self.mostrar_mensaje("Error", "La cantidad de números tiene que ser mayor a cero")
			return
		self.mu = mu
		self.sigma = sigma
		self.lambd = lambd

		# Genero variables aleatorias dependiendo del tipo de distribucion seleccionado
		if id_tipo_distribucion == 0:
			self.variables_aleatorias = self.controlador.generar_variables_aleatorias_normal(mu, sigma,
																							 cantidad_numeros)
		elif id_tipo_distribucion == 1:
			self.variables_aleatorias = self.controlador.generar_variables_aleatorias_exponencial(lambd,
																								  cantidad_numeros)
		elif id_tipo_distribucion == 2:
			self.variables_aleatorias = self.controlador.generar_variables_aleatorias_poisson(lambd, cantidad_numeros)
		self.tipo_distribucion = id_tipo_distribucion

		# Cargo tabla
		self.cargar_tabla_variables_aleatorias()

	def accion_limpiar_interfaz_prueba_frecuencia(self):

		# Llamo a metodo limpiar interfaz de prueba frecuencia
		self.limpiar_interfaz_prueba_frecuencia()

	def accion_generar_grafico(self):

		# Valido que se hayan generado variables aleatorias con anterioridad
		if len(self.variables_aleatorias) == 0:
			self.mostrar_mensaje("Error", "Primero debe generar las variables aleatorias")
			return

		# Obtengo y valido parametros
		cantidad_intervalos = self.txt_cantidad_intervalos.text()
		if cantidad_intervalos == "" or int(cantidad_intervalos) <= 0:
			self.mostrar_mensaje("Error", "La cantidad de intervalos tiene que ser mayor a cero")
			return

		# Muestro grafico de frecuencias
		self.controlador.generar_grafico_frecuencias(self.variables_aleatorias, cantidad_intervalos)

	def accion_test_chi_cuadrado(self):

		# Valido que se hayan generado variables aleatorias con anterioridad
		if len(self.variables_aleatorias) == 0:
			self.mostrar_mensaje("Error", "Primero debe generar las variables aleatorias")
			return

		# Obtengo y valido parametros
		cantidad_intervalos = self.txt_cantidad_intervalos.text()
		if cantidad_intervalos == "" or int(cantidad_intervalos) <= 0:
			self.mostrar_mensaje("Error", "La cantidad de intervalos tiene que ser mayor a cero")
			return

		# Obtengo listas de medias, frecuencias observadas y frecuencias esperadas
		medias, observadas, esperadas = self.controlador.calcular_frecuencias_por_intervalo(self.variables_aleatorias,
																							cantidad_intervalos,
																							self.tipo_distribucion,
																							self.mu, self.sigma,
																							self.lambd)

		# Realizo prueba de chi cuadrado y muestro resultados
		chi_cuadrado = self.controlador.test_chi_cuadrado(observadas, esperadas)
		self.mostrar_mensaje("Valor obtenido", "El valor de Chi cuadrado obtenido es %s"
							 % str(chi_cuadrado).replace(".", ","))

	""" Metodos """

	def preparar_interfaz(self):

		# Cargo combo box
		self.cmb_tipo_distribucion.clear()
		self.cmb_tipo_distribucion.addItem("Distribución Normal", 0)
		self.cmb_tipo_distribucion.addItem("Distribución Exponencial", 1)
		self.cmb_tipo_distribucion.addItem("Distribución Poisson", 2)

		# Preparo tabla de variables generadas
		self.grid_variables_generadas.setColumnCount(2)
		self.grid_variables_generadas.setHorizontalHeaderLabels(["Nro de orden", "Variable aleatoria"])

	def limpiar_interfaz_generar_variables(self):

		# Limpio txts
		self.txt_mu.clear()
		self.txt_sigma.clear()
		self.txt_lambda.clear()
		self.txt_cantidad_variables.clear()

		# Selecciono opcion por defecto en combo boxs
		self.cmb_tipo_distribucion.setCurrentIndex(0)

		# Limpio grilla
		self.grid_variables_generadas.clearSelection()
		self.grid_variables_generadas.setCurrentCell(-1, -1)
		self.grid_variables_generadas.setRowCount(0)

	def limpiar_interfaz_prueba_frecuencia(self):

		# Limpio txts
		self.txt_cantidad_intervalos.clear()

	def mostrar_mensaje(self, titulo, mensaje):

		# Muestro mensaje
		box = QMessageBox()
		box.setWindowTitle(titulo)
		box.setText(mensaje)
		box.setStandardButtons(QMessageBox.Ok)
		box.exec_()

	def cargar_tabla_variables_aleatorias(self):

		self.grid_variables_generadas.setRowCount(len(self.variables_aleatorias))
		index = 0
		for va in self.variables_aleatorias:

			# Obtengo datos en formato conveniente
			nro_orden = str(va.get("nro_orden"))
			variable_aleatoria = str(va.get("variable_aleatoria")).replace(".", ",")

			# Agrego fila a tabla
			self.grid_variables_generadas.setItem(index, 0, QTableWidgetItem(nro_orden))
			self.grid_variables_generadas.setItem(index, 1, QTableWidgetItem(variable_aleatoria))
			index += 1

	""" Eventos """

	# Evento show
	def showEvent(self, QShowEvent):
		self.preparar_interfaz()
		self.limpiar_interfaz_generar_variables()
		self.limpiar_interfaz_prueba_frecuencia()
