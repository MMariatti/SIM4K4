from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from dominio.controlador_generador_numeros import ControladorGeneradorNumeros
from soporte.validador_decimales import ValidadorDecimales
from soporte.validador_enteros import ValidadorEnteros
from soporte.ruta import Ruta


class VentanaGeneradorNumeros(QMainWindow):

	""" Atributos """

	controlador = None
	numeros_aleatorios = []

	""" Constructor """

	def __init__(self):
		# Genero ventana a partir de ui y creo controlador
		QMainWindow.__init__(self)
		uic.loadUi(Ruta.generar_ruta("interfaz/ventana_generador_numeros.ui"), self)
		self.controlador = ControladorGeneradorNumeros()

		# Agrego validadores a los campos
		validador_decimales = ValidadorDecimales(12, 4)
		validador_enteros = ValidadorEnteros(12)
		self.txt_semilla.setValidator(validador_decimales)
		self.txt_a.setValidator(validador_decimales)
		self.txt_c.setValidator(validador_decimales)
		self.txt_m.setValidator(validador_decimales)
		self.txt_cantidad_numeros.setValidator(validador_enteros)
		self.txt_cantidad_intervalos.setValidator(validador_enteros)

		# Conecto los botones con los eventos
		self.cmb_metodo_generacion.currentIndexChanged.connect(self.accion_seleccionar_metodo)
		self.btn_limpiar_generar_numeros.clicked.connect(self.accion_limpiar_interfaz_generar_numeros)
		self.btn_generar_numeros.clicked.connect(self.accion_generar_numeros)
		self.btn_limpiar_prueba_frecuencia.clicked.connect(self.accion_limpiar_interfaz_prueba_frecuencia)
		self.btn_prueba_frecuencia.clicked.connect(self.accion_prueba_frecuencia)

	""" Acciones """

	def accion_seleccionar_metodo(self):

		# Activo o desactivo input de constante c dependiendo del metodo elegido
		id_metodo = self.cmb_metodo_generacion.itemData(self.cmb_metodo_generacion.currentIndex())
		if id_metodo == 0:
			self.txt_semilla.setEnabled(True)
			self.txt_a.setEnabled(True)
			self.txt_c.setEnabled(True)
			self.txt_m.setEnabled(True)
		elif id_metodo == 1:
			self.txt_semilla.setEnabled(True)
			self.txt_a.setEnabled(True)
			self.txt_c.clear()
			self.txt_c.setEnabled(False)
			self.txt_m.setEnabled(True)
		else:
			self.txt_semilla.clear()
			self.txt_semilla.setEnabled(False)
			self.txt_a.clear()
			self.txt_a.setEnabled(False)
			self.txt_c.clear()
			self.txt_c.setEnabled(False)
			self.txt_m.clear()
			self.txt_m.setEnabled(False)

	def accion_limpiar_interfaz_generar_numeros(self):

		# Limpio lista de numeros aleatorioz
		self.numeros_aleatorios = []

		# Llamo a metodo limpiar interfaz de generar numeros
		self.limpiar_interfaz_generar_numeros()

	def accion_generar_numeros(self):

		# Obtengo metodo
		id_metodo = self.cmb_metodo_generacion.itemData(self.cmb_metodo_generacion.currentIndex())

		# Obtengo y valido parametros dependiendo del metodo
		semilla = None
		a = None
		c = None
		m = None
		if id_metodo == 0 or id_metodo == 1:
			semilla = self.txt_semilla.text()
			if semilla == "" or float(semilla.replace(",", ".")) < 0:
				self.mostrar_mensaje("Error", "La semilla tiene que ser mayor o igual a cero")
				return
			a = self.txt_a.text()
			if a == "" or float(a.replace(",", ".")) <= 0:
				self.mostrar_mensaje("Error", "La constante \"a\" tiene que ser mayor a cero")
				return
		if id_metodo == 0:
			c = self.txt_c.text()
			if c == "" or float(c.replace(",", ".")) <= 0:
				self.mostrar_mensaje("Error", "La constante \"c\" tiene que ser mayor a cero")
				return
		if id_metodo == 0 or id_metodo == 1:
			m = self.txt_m.text()
			if m == "" or float(m.replace(",", ".")) <= 0:
				self.mostrar_mensaje("Error", "La constante \"m\" tiene que ser mayor a cero")
				return
			if float(semilla.replace(",", ".")) >= float(m.replace(",", ".")):
				self.mostrar_mensaje("Error", "La semilla tiene que ser menor a la constante \"m\"")
				return
			if float(a.replace(",", ".")) >= float(m.replace(",", ".")):
				self.mostrar_mensaje("Error", "La constante \"a\" tiene que ser menor a la constante \"m\"")
				return
			if id_metodo == 0:
				if float(c.replace(",", ".")) >= float(m.replace(",", ".")):
					self.mostrar_mensaje("Error", "La constante \"c\" tiene que ser menor a la constante \"m\"")
					return
		cantidad_numeros = self.txt_cantidad_numeros.text()
		if cantidad_numeros == "" or int(cantidad_numeros) <= 0:
			self.mostrar_mensaje("Error", "La cantidad de números tiene que ser mayor a cero")
			return

		# Genero numeros aleatorios dependiendo del metodo seleccionado
		if id_metodo == 0:
			self.numeros_aleatorios = self.controlador.generar_numeros_congruente_mixo(
				cantidad_numeros, semilla, a, c, m)
		elif id_metodo == 1:
			self.numeros_aleatorios = self.controlador.generar_numeros_congruente_multiplicativo(
				cantidad_numeros, semilla, a, m)
		elif id_metodo == 2:
			self.numeros_aleatorios = self.controlador.generar_numeros_provisto_por_lenguaje(cantidad_numeros)

		# Cargo tabla
		self.cargar_tabla_numeros_aleatorios()

	def accion_limpiar_interfaz_prueba_frecuencia(self):

		# Llamo a metodo limpiar interfaz de prueba frecuencia
		self.limpiar_interfaz_prueba_frecuencia()

	def accion_prueba_frecuencia(self):

		# Valido que se hayan generado numeros aleatorios con anterioridad
		if len(self.numeros_aleatorios) == 0:
			self.mostrar_mensaje("Error", "Primero debe generar los números aleatorios")
			return

		# Obtengo y valido parametros
		cantidad_intervalos = self.txt_cantidad_intervalos.text()
		if cantidad_intervalos == "" or int(cantidad_intervalos) <= 0:
			self.mostrar_mensaje("Error", "La cantidad de intervalos tiene que ser mayor a cero")
			return

		# Obtengo listas de medias, frecuencias observadas y frecuencias esperadas
		medias, observadas, esperadas = self.controlador.calcular_frecuencias_por_intervalo(self.numeros_aleatorios,
																							cantidad_intervalos)

		# Realizo prueba de chi cuadrado y muestro resultados
		chi_cuadrado = self.controlador.prueba_chicuadrado(observadas, esperadas)
		self.mostrar_mensaje("Valor obtenido", "El valor de Chi cuadrado obtenido es %s"
							 % str(chi_cuadrado).replace(".", ","))

		# Muestro grafico de frecuencias
		self.controlador.generar_grafico_frecuencias(medias, observadas, esperadas)

	""" Metodos """

	def preparar_interfaz(self):

		# Cargo combo box
		self.cmb_metodo_generacion.clear()
		self.cmb_metodo_generacion.addItem("Método congruente mixto", 0)
		self.cmb_metodo_generacion.addItem("Método congruente multiplicativo", 1)
		self.cmb_metodo_generacion.addItem("Método provisto por el lenguaje", 2)

		# Preparo tabla de numeros generados
		self.grid_numeros_generados.setColumnCount(3)
		self.grid_numeros_generados.setHorizontalHeaderLabels(["N° de orden", "Semilla", "Número aleatorio"])

	def limpiar_interfaz_generar_numeros(self):

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

	def cargar_tabla_numeros_aleatorios(self):

		self.grid_numeros_generados.setRowCount(len(self.numeros_aleatorios))
		index = 0
		for n in self.numeros_aleatorios:

			# Obtengo datos en formato conveniente
			nro_orden = str(n.get("nro_orden"))
			semilla = n.get("semilla")
			if semilla is not None:
				if int(semilla) == semilla:
					semilla = int(semilla)
				semilla = str(semilla).replace(".", ",")
			else:
				semilla = ""
			aleatorio_decimal = str(n.get("aleatorio_decimal")).replace(".", ",")

			# Agrego fila a tabla
			self.grid_numeros_generados.setItem(index, 0, QTableWidgetItem(nro_orden))
			self.grid_numeros_generados.setItem(index, 1, QTableWidgetItem(semilla))
			self.grid_numeros_generados.setItem(index, 2, QTableWidgetItem(aleatorio_decimal))
			index += 1

	""" Eventos """

	# Evento show
	def showEvent(self, QShowEvent):
		self.preparar_interfaz()
		self.limpiar_interfaz_generar_numeros()
		self.limpiar_interfaz_prueba_frecuencia()
