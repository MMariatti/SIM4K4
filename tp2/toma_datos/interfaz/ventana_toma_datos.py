from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from dominio.controlador_toma_datos import ControladorTomaDatos
from soporte.validador_enteros import ValidadorEnteros
from soporte.ruta import Ruta


class VentanaTomaDatos(QMainWindow):

    """ Atributos """

    controlador = None
    variables_aleatorias = []

    """ Constructor """

    def __init__(self):

        # Genero ventana a partir de ui y creo controlador
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("interfaz/ventana_toma_datos.ui"), self)
        self.controlador = ControladorTomaDatos()

        # Agrego validadores a los campos
        validador_enteros = ValidadorEnteros(2)
        self.txt_columna.setValidator(validador_enteros)
        self.txt_fila_desde.setValidator(validador_enteros)
        self.txt_fila_hasta.setValidator(validador_enteros)

        # Conecto los botones con los eventos
        self.btn_seleccionar_archivo.clicked.connect(self.accion_seleccionar_archivo)
        self.btn_generar_histograma.clicked.connect(self.accion_generar_histograma)
        self.btn_prueba_1.clicked.connect(self.accion_prueba_1)  # TODO: No definido
        self.btn_prueba_1.clicked.connect(self.accion_prueba_2)  # TODO: No definido

    """ Acciones """

    def accion_seleccionar_archivo(self):
        pass

    def accion_generar_histograma(self):

        # TODO: Harcodeo lista de variables aleatorias para probar
        self.variables_aleatorias = [10, 20, 20, 30, 30, 30, 40, 40, 40, 40, 50, 50, 50, 50, 50, 60, 60, 60, 60, 70, 70,
                                     70, 80, 80, 90]

        # Valido que se hayan obtenido las variables aleatorias con anterioridad
        if len(self.variables_aleatorias) == 0:
            self.mostrar_mensaje("Error", "Primero deben obtener las variables aleatorias")
            return

        """
        # Obtengo y valido parametros
        cantidad_intervalos = self.txt_cantidad_intervalos.text()
        if cantidad_intervalos == "" or int(cantidad_intervalos) <= 0:
            self.mostrar_mensaje("Error", "La cantidad de intervalos tiene que ser mayor a cero")
            return
        """

        # Obtengo listas de medias y frecuencias
        # TODO: Harcodeo cantidad de intervalos hasta que se agregue a interfaz
        medias, frecuencias = self.controlador.calcular_frecuencias_por_intervalo(self.variables_aleatorias, 10)

        # Muestro histograma
        self.controlador.generar_grafico_frecuencias(medias, frecuencias)

    # TODO: No definido
    def accion_prueba_1(self):
        pass

    # TODO: No definido
    def accion_prueba_2(self):
        pass

    """ Metodos """

    def limpiar_interfaz(self):

        # Limpio txts
        self.txt_columna.clear()
        self.txt_fila_desde.clear()
        self.txt_fila_hasta.clear()

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
        self.limpiar_interfaz()
