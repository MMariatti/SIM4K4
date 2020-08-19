from os.path import expanduser
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5 import uic
from dominio.controlador_toma_datos import ControladorTomaDatos
from soporte.validador_enteros import ValidadorEnteros
from soporte.ruta import Ruta


class VentanaTomaDatos(QMainWindow):

    """ Atributos """

    controlador = None
    ruta_archivo = None
    variables_aleatorias = []

    """ Constructor """

    def __init__(self):

        # Genero ventana a partir de ui y creo controlador
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("interfaz/ventana_toma_datos.ui"), self)
        self.controlador = ControladorTomaDatos()

        # Agrego validadores a los campos
        validador_enteros = ValidadorEnteros(9)
        self.txt_columna.setValidator(validador_enteros)
        self.txt_fila_desde.setValidator(validador_enteros)
        self.txt_fila_hasta.setValidator(validador_enteros)

        # Conecto los botones con los eventos
        self.btn_seleccionar_archivo.clicked.connect(self.accion_seleccionar_archivo)
        self.btn_obtener_datos.clicked.connect(self.accion_obtener_datos)
        self.btn_generar_histograma.clicked.connect(self.accion_generar_histograma)
        self.btn_prueba_1.clicked.connect(self.accion_prueba_1)  # TODO: No definido
        self.btn_prueba_1.clicked.connect(self.accion_prueba_2)  # TODO: No definido

    """ Acciones """

    def accion_seleccionar_archivo(self):

        # Obtengo ruta del xlxs
        self.ruta_archivo = QFileDialog.getOpenFileName(self, "Seleccione su archivo de datos", expanduser("~"),
                                                        "Excel (*.xls *.xlsx)")[0]

    def accion_obtener_datos(self):

        # Obtengo y valido parametros
        if self.ruta_archivo is None or self.ruta_archivo == "":
            self.mostrar_mensaje("Error", "Debe seleccionar un archivo")
            return
        columna = self.txt_columna.text()
        if columna == "" or int(columna) <= 0:
            self.mostrar_mensaje("Error", "El número de columna de donde tomar los datos debe ser mayor a cero")
            return
        fila_desde = self.txt_fila_desde.text()
        if fila_desde == "" or int(fila_desde) <= 0:
            self.mostrar_mensaje("Error", "El número de fila desde donde tomar los datos debe ser mayor a cero")
            return
        fila_hasta = self.txt_fila_hasta.text()
        if fila_hasta == ""or int(fila_hasta) <= 0:
            self.mostrar_mensaje("Error", "El número de fila hasta donde tomar los datos debe ser mayor a cero")
            return

        # Obtengo variables aleatorias desde archivo
        try:
            self.variables_aleatorias = self.controlador.obtener_variables_aleatorias(self.ruta_archivo, columna,
                                                                                      fila_desde, fila_hasta)
            self.mostrar_mensaje("Valores obtenidos", "Se obtuvieron correctamente %s valores" %
                                 len(self.variables_aleatorias))

        except Exception as ex:
            self.mostrar_mensaje("Error", "Hubo un problema al obtener los datos del archivo")
            print(ex)

    def accion_generar_histograma(self):

        # Valido que se hayan obtenido las variables aleatorias con anterioridad
        if len(self.variables_aleatorias) == 0:
            self.mostrar_mensaje("Error", "Primero deben obtener las variables aleatorias")
            return

        # Obtengo y valido parametros
        cantidad_intervalos = self.txt_cantidad_intervalos.text()
        if cantidad_intervalos == "" or int(cantidad_intervalos) <= 0:
            self.mostrar_mensaje("Error", "La cantidad de intervalos tiene que ser mayor a cero")
            return
        tipo_distribucion = self.cmb_tipo_distribucion.itemData(self.cmb_tipo_distribucion.currentIndex())
        if tipo_distribucion == -1:
            self.mostrar_mensaje("Error", "Debe seleccionar un tipo de distribución")
            return

        # Obtengo listas de medias, frecuencias observadas y frecuencias esperadas
        medias, observadas, esperadas = self.controlador.calcular_frecuencias_por_intervalo(self.variables_aleatorias,
                                                                                            cantidad_intervalos,
                                                                                            tipo_distribucion)

        # Muestro histograma
        self.controlador.generar_histograma(medias, observadas)

    # TODO: No definido
    def accion_prueba_1(self):
        pass

    # TODO: No definido
    def accion_prueba_2(self):
        pass

    """ Metodos """

    def preparar_interfaz(self):

        # Cargo combo box
        self.cmb_tipo_distribucion.clear()
        self.cmb_tipo_distribucion.addItem("Seleccione", -1)
        self.cmb_tipo_distribucion.addItem("Uniforme", 0)
        self.cmb_tipo_distribucion.addItem("Normal", 1)
        self.cmb_tipo_distribucion.addItem("Exponencial negativa", 2)

    def limpiar_interfaz(self):

        # Limpio txts
        self.txt_columna.clear()
        self.txt_fila_desde.clear()
        self.txt_fila_hasta.clear()

        # Selecciono opcion por defecto en combo boxs
        self.cmb_tipo_distribucion.setCurrentIndex(0)

    def mostrar_mensaje(self, titulo, mensaje):

        # Muestro mensaje
        box = QMessageBox()
        box.setWindowTitle(titulo)
        box.setText(mensaje)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()

    """ Eventos """

    # Evento show
    def showEvent(self, QShowEvent):
        self.preparar_interfaz()
        self.limpiar_interfaz()
