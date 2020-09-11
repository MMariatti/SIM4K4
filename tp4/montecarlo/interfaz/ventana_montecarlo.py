from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.Qt import QHeaderView
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
        self.txt_dia_visualizacion.textChanged.connect(self.accion_seleccionar_dia_visualizacion)

    """ Acciones """

    def accion_limpiar_interfaz(self):

        # Limpio lista de dias simulados
        self.dias_simulados = []

        # Llamo a metodo limpiar interfaz
        self.limpiar_interfaz()

    def accion_simular(self):

        # Obtengo y valido parametros
        frascos_a_comprar = self.txt_frascos_a_comprar.text()
        if frascos_a_comprar == "" or int(frascos_a_comprar.replace(",", ".")) <= 0:
            self.mostrar_mensaje("Error", "La cantidad de frascos a comprar debe ser mayor a cero")
            return
        dias_cada_cuanto_comprar = self.txt_dias_cada_cuanto_comprar.text()
        if dias_cada_cuanto_comprar == "" or int(dias_cada_cuanto_comprar.replace(",", ".")) <= 0:
            self.mostrar_mensaje("Error", "Los cantidad de días cada cuanto comprar debe ser mayor a cero")
            return
        peso_frasco = self.txt_peso_frasco.text()
        if peso_frasco == "" or int(peso_frasco.replace(",", ".")) <= 0:
            self.mostrar_mensaje("Error", "El peso por cada frasco debe ser mayor a cero")
            return
        capacidad_maxima_frascos = self.txt_capacidad_maxima_frascos.text()
        if capacidad_maxima_frascos == "" or int(capacidad_maxima_frascos) <= 0:
            self.mostrar_mensaje("Error", "La capacidad máxima de frascos a almacenar tiene que ser mayor a cero")
            return
        mu_normal = self.txt_mu_normal.text()
        if mu_normal == "":
            self.mostrar_mensaje("Error", "La constante \"mu\" de la distribución normal no puede ser vacía")
            return
        sigma_normal = self.txt_sigma_normal.text()
        if sigma_normal == "" or float(sigma_normal.replace(",", ".")) < 0:
            self.mostrar_mensaje("Error", "La constante \"sigma\" de la distribución normal tiene que ser mayor o "
                                          "igual a cero")
            return
        mu_exponencial = self.txt_mu_exponencial.text()
        if mu_exponencial == "":
            self.mostrar_mensaje("Error", "La constante \"mu\" de la distribución exponencial no puede ser vacía")
            return
        horas_maniana = self.txt_horas_maniana.text()
        if horas_maniana == "" or int(horas_maniana.replace(",", ".")) <= 0:
            self.mostrar_mensaje("Error", "Las cantidad de horas del turno mañana debe ser mayor a cero")
            return
        horas_tarde = self.txt_horas_tarde.text()
        if horas_tarde == "" or int(horas_tarde.replace(",", ".")) <= 0:
            self.mostrar_mensaje("Error", "Las cantidad de horas del turno tarde debe ser mayor a cero")
            return
        id_tipo_generador = self.cmb_tipo_generador.itemData(self.cmb_tipo_generador.currentIndex())
        dias = self.txt_dias.text()
        if dias == "" or int(dias.replace(",", ".")) <= 0:
            self.mostrar_mensaje("Error", "La cantidad de días a simular debe ser mayor a cero")
            return

        # Genero diccionario con parametros para la simulacion
        parametros = {
            "frascos_a_comprar": frascos_a_comprar,
            "dias_cada_cuanto_comprar": dias_cada_cuanto_comprar,
            "peso_frasco": peso_frasco,
            "capacidad_maxima_frascos": capacidad_maxima_frascos,
            "mu_normal": mu_normal,
            "sigma_normal": sigma_normal,
            "mu_exponencial": mu_exponencial,
            "horas_maniana": horas_maniana,
            "horas_tarde": horas_tarde,
            "id_tipo_generador": id_tipo_generador,
            "dias": dias
        }

        # Simulo dias
        self.dias_simulados, resultados = self.controlador.simular(parametros)

        # Cargo resultados
        self.cargar_resultados_simulacion(resultados)

        # Cargo tabla
        self.cargar_tabla_dias_simulados()

    def accion_seleccionar_tipo_visualizacion(self):

        # Activo o desactivo inputs dependiendo del tipo de visualizacion elegido
        id_tipo_visualizacion = self.cmb_tipo_visualizacion.itemData(self.cmb_tipo_visualizacion.currentIndex())
        if id_tipo_visualizacion == 0:
            self.txt_dia_visualizacion.clear()
            self.txt_dia_visualizacion.setEnabled(False)
        else:
            self.txt_dia_visualizacion.setText("1")
            self.txt_dia_visualizacion.setEnabled(True)

        # Cargo tabla si hay dias simulados
        if len(self.dias_simulados):
            self.cargar_tabla_dias_simulados()

    def accion_seleccionar_dia_visualizacion(self):

        # Cargo tabla si hay dias simulados
        if len(self.dias_simulados):
            self.cargar_tabla_dias_simulados()

    """ Metodos """

    def preparar_interfaz(self):

        # Cargo combo boxs
        self.cmb_tipo_generador.clear()
        self.cmb_tipo_generador.addItem("Provisto por el lenguaje", 0)
        self.cmb_tipo_generador.addItem("Congruencial mixto", 1)
        self.cmb_tipo_visualizacion.clear()
        self.cmb_tipo_visualizacion.addItem("Cada 1000 días", 0)
        self.cmb_tipo_visualizacion.addItem("50 días a partir de día seleccionado", 1)

        # Preparo tabla de numeros generados
        self.grid_dias_simulados.setColumnCount(8)
        self.grid_dias_simulados.setHorizontalHeaderLabels(["Día", "Stock al finalizar día", "Café almacenado promedio",
                                                            "Café faltante promedio", "Ingreso", "Ingreso promedio",
                                                            "Contribución", "Contribución promedio"])
        header = self.grid_dias_simulados.horizontalHeader()
        for i in range(0, 8):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

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

    def mostrar_mensaje(self, titulo, mensaje):

        # Muestro mensaje
        box = QMessageBox()
        box.setWindowTitle(titulo)
        box.setText(mensaje)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()

    def cargar_resultados_simulacion(self, resultados):

        # Obtengo datos en formato conveniente
        porcentaje_dias_faltantes = str(resultados.get("porcentaje_dias_faltantes")).replace(".", ",")
        porcentaje_dias_0_a_2_frascos = str(resultados.get("porcentaje_dias_0_a_2_frascos")).replace(".", ",")
        porcentaje_dias_2_a_5_frascos = str(resultados.get("porcentaje_dias_2_a_5_frascos")).replace(".", ",")
        porcentaje_dias_5_a_8_frascos = str(resultados.get("porcentaje_dias_5_a_8_frascos")).replace(".", ",")
        porcentaje_dias_mas_8_frascos = str(resultados.get("porcentaje_dias_mas_8_frascos")).replace(".", ",")
        promedio_horas_perdidas = str(resultados.get("promedio_horas_perdidas")).replace(".", ",")
        tiene_stock = "Si" if resultados.get("tiene_stock") else "No"

        # Cargo txts de resultados
        self.txt_porcentaje_dias_faltantes.setText(porcentaje_dias_faltantes)
        self.txt_porcentaje_dias_0_a_2_frascos.setText(porcentaje_dias_0_a_2_frascos)
        self.txt_porcentaje_dias_2_a_5_frascos.setText(porcentaje_dias_2_a_5_frascos)
        self.txt_porcentaje_dias_5_a_8_frascos.setText(porcentaje_dias_5_a_8_frascos)
        self.txt_porcentaje_dias_mas_8_frascos.setText(porcentaje_dias_mas_8_frascos)
        self.txt_promedio_horas_perdidas.setText(promedio_horas_perdidas)
        self.txt_tiene_stock.setText(tiene_stock)

    def cargar_tabla_dias_simulados(self):

        # Obtengo indices a renderizar y cantidad de filas dependiendo del tipo de visualizacion
        indices_filas = []
        id_tipo_visualizacion = self.cmb_tipo_visualizacion.itemData(self.cmb_tipo_visualizacion.currentIndex())
        if id_tipo_visualizacion == 0:
            indices_filas.append(0)
            indice = 999
            while indice <= len(self.dias_simulados) - 1:
                indices_filas.append(indice)
                indice += 1000
            cantidad_filas = 1 + ((len(self.dias_simulados)) // 1000)

        else:
            dia_visualizacion = self.txt_dia_visualizacion.text()
            if dia_visualizacion == "" or int(dia_visualizacion) == 0:
                self.txt_dia_visualizacion.setText("1")
                dia_visualizacion = 1
            else:
                dia_visualizacion = int(dia_visualizacion)
            for i in range(0, 50):
                if dia_visualizacion - 1 + i >= len(self.dias_simulados):
                    break
                indices_filas.append(dia_visualizacion - 1 + i)
            cantidad_filas = len(indices_filas)

        # Cargo tabla
        self.grid_dias_simulados.setRowCount(cantidad_filas)
        index = 0
        for i in indices_filas:

            # Obtendo dato de lista
            ds = self.dias_simulados[i]

            # Obtengo datos en formato conveniente
            nro_dia = str(ds.get("nro_dia"))
            stock = str(ds.get("stock"))
            cafe_almacenado_promedio = str(ds.get("cafe_almacenado_promedio")).replace(".", ",")
            cafe_faltante_promedio = str(ds.get("cafe_faltante_promedio")).replace(".", ",")
            ingreso = str(ds.get("ingreso")).replace(".", ",")
            ingreso_promedio = str(ds.get("ingreso_promedio")).replace(".", ",")
            contribucion = str(ds.get("contribucion")).replace(".", ",")
            contribucion_promedio = str(ds.get("contribucion_promedio")).replace(".", ",")

            # Agrego fila a tabla
            self.grid_dias_simulados.setItem(index, 0, QTableWidgetItem(nro_dia))
            self.grid_dias_simulados.setItem(index, 1, QTableWidgetItem(stock))
            self.grid_dias_simulados.setItem(index, 2, QTableWidgetItem(cafe_almacenado_promedio))
            self.grid_dias_simulados.setItem(index, 3, QTableWidgetItem(cafe_faltante_promedio))
            self.grid_dias_simulados.setItem(index, 4, QTableWidgetItem(ingreso))
            self.grid_dias_simulados.setItem(index, 5, QTableWidgetItem(ingreso_promedio))
            self.grid_dias_simulados.setItem(index, 6, QTableWidgetItem(contribucion))
            self.grid_dias_simulados.setItem(index, 7, QTableWidgetItem(contribucion_promedio))
            index += 1

    # Evento show
    def showEvent(self, QShowEvent):

        self.preparar_interfaz()
        self.limpiar_interfaz()

