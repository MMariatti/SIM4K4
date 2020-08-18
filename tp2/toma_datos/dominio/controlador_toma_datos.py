import xlrd


class ControladorTomaDatos:

    def obtener_variables_aleatorias(self, ruta_archivo, columna, fila_desde, fila_hasta):

        # Adapto parametros para usarlos con libreria
        columna = columna - 1
        fila_desde = fila_desde - 1
        fila_hasta = fila_hasta - 1

        # Inicializo lista
        variables_aleatorias = []

        # Obtengo planilla
        file = xlrd.open_workbook(ruta_archivo)
        hoja = file.sheet_by_index(0)

        # Guardo valores en lista
        for i in range(fila_desde, fila_hasta + 1):
            valor = round(float(hoja.cell_value(i, columna)), 4)
            if valor == int(valor):
                valor = int(valor)
            variables_aleatorias.append(valor)

        return variables_aleatorias

    def calcular_frecuencias_por_intervalo(self, variables_aleatorias, cantidad_intervalos):
        pass

    def generar_grafico_frecuencias(self, medias, frecuencias):
        pass
