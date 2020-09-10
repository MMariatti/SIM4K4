from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from dominio.controlador_montecarlo import ControladorMontecarlo
from soporte.validador_decimales import ValidadorDecimales
from soporte.validador_enteros import ValidadorEnteros
from soporte.ruta import Ruta


class VentanaMontecarlo(QMainWindow):

    """ Atributos """

    controlador = None
    dias_simulados = []

    """ Constructor """

    def __init__(self):

        # Genero ventana a partir de ui y creo controlador
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("interfaz/ventana_montecarlo.ui"), self)
        self.controlador = ControladorMontecarlo()

        # Agrego validadores a los campos
        validador_decimales_negativos = ValidadorDecimales(7, 4, negative=True)
        validador_decimales = ValidadorDecimales(7, 4)
        validador_enteros = ValidadorEnteros(7)
        self.txt_frascos_a_comprar.setValidator(validador_enteros)
        self.txt_dias_cada_cuanto_comprar.setValidator(validador_enteros)
        self.txt_peso_frasco.setValidator(validador_enteros)
        self.txt_capacidad_maxima_frascos.setValidator(validador_enteros)
        self.txt_mu_normal.setValidator(validador_decimales_negativos)
        self.txt_sigma_normal.setValidator(validador_decimales)
        self.txt_mu_exponencial.setValidator(validador_decimales)
        self.txt_horas_maniana.setValidator(validador_enteros)
        self.txt_horas_tarde.setValidator(validador_enteros)
        self.txt_dias.setValidator(validador_enteros)
        self.txt_dia_visualizacion.setValidator(validador_enteros)

        # Conecto los botones con los eventos
        self.btn_limpiar.clicked.connect(self.accion_limpiar_interfaz)
        self.btn_simular.clicked.connect(self.accion_simular)
        self.cmb_tipo_visualizacion.currentIndexChanged.connect(self.accion_seleccionar_tipo_visualizacion)

    """ Acciones """

    def accion_limpiar_interfaz(self):

        # Limpio lista de dias simulados
        self.dias_simulados = []

        # Llamo a metodo limpiar interfaz
        self.limpiar_interfaz()

    def accion_simular(self):
        pass

    def accion_seleccionar_tipo_visualizacion(self):

        # Activo o desactivo inputs dependiendo del tipo de visualizacion elegido
        id_tipo_visualizacion = self.cmb_tipo_visualizacion.itemData(self.cmb_tipo_visualizacion.currentIndex())
        if id_tipo_visualizacion == 0:
            self.txt_dia_visualizacion.clear()
            self.txt_dia_visualizacion.setEnabled(False)
        else:
            self.txt_dia_visualizacion.setEnabled(True)

    """ Metodos """

    def preparar_interfaz(self):

        # Cargo combo boxs
        self.cmb_tipo_generador.clear()
        self.cmb_tipo_generador.addItem("Provisto por el lenguaje", 0)
        self.cmb_tipo_generador.addItem("Congruencial", 1)
        self.cmb_tipo_visualizacion.clear()
        self.cmb_tipo_visualizacion.addItem("Cada 1000 días", 0)
        self.cmb_tipo_visualizacion.addItem("50 días a partir de día seleccionado", 1)

        # Preparo tabla de numeros generados
        self.grid_dias_simulados.setColumnCount(5)
        self.grid_dias_simulados.setHorizontalHeaderLabels([])

    def limpiar_interfaz(self):

        # Limpio txts
        self.txt_frascos_a_comprar.clear()
        self.txt_frascos_a_comprar.setText("2")
        self.txt_dias_cada_cuanto_comprar.clear()
        self.txt_dias_cada_cuanto_comprar.setText("2")
        self.txt_peso_frasco.clear()
        self.txt_peso_frasco.setText("170")
        self.txt_capacidad_maxima_frascos.clear()
        self.txt_capacidad_maxima_frascos.setText("10")
        self.txt_mu_normal.clear()
        self.txt_mu_normal.setText("75")
        self.txt_sigma_normal.clear()
        self.txt_sigma_normal.setText("15")
        self.txt_mu_exponencial.clear()
        self.txt_mu_exponencial.setText("70")
        self.txt_horas_maniana.clear()
        self.txt_horas_maniana.setText("8")
        self.txt_horas_tarde.clear()
        self.txt_horas_tarde.setText("8")
        self.txt_dias.clear()
        self.txt_dia_visualizacion.clear()
        self.txt_porcentaje_dias_faltantes.clear()
        self.txt_porcentaje_dias_0_a_2_frascos.clear()
        self.txt_porcentaje_dias_2_a_5_frascos.clear()
        self.txt_porcentaje_dias_5_a_8_frascos.clear()
        self.txt_porcentaje_dias_mas_8_frascos.clear()
        self.txt_promedio_horas_perdidas.clear()
        self.txt_tiene_stock.clear()

        # Deshabilito txts
        self.txt_dia_visualizacion.setEnabled(False)

        # Selecciono opcion por defecto en combo boxs
        self.cmb_tipo_generador.setCurrentIndex(0)
        self.cmb_tipo_visualizacion.setCurrentIndex(0)

        # Limpio grilla
        self.grid_dias_simulados.clearSelection()
        self.grid_dias_simulados.setCurrentCell(-1, -1)
        self.grid_dias_simulados.setRowCount(0)

    """ Eventos """

    # Evento show
    def showEvent(self, QShowEvent):

        self.preparar_interfaz()
        self.limpiar_interfaz()

