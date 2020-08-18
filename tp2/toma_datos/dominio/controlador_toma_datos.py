import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
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
        # Convierto tipos de datos
        cantidad_intervalos = int(cantidad_intervalos)

        # Inicializo datos
        min = MIN(variables_aleatorias)
        max = MAX(variables_aleatorias)
        paso = (max - min) / cantidad_intervalos
        intervalos = []
        frecuencias_x_intervalo = {}

        # Genero lista de intervalos e inicializo keys en diccionario de frecuencias por intervalo
        for i in range(0, cantidad_intervalos):
            min_intervalo = round(min, 4)
            max_intervalo = round(min_intervalo + paso, 4)
            media_intervalo = round(((min_intervalo + max_intervalo) / 2), 4)
            intervalos.append({
                "minimo": min_intervalo,
                "maximo": max_intervalo,
                "media": media_intervalo
            })
            frecuencias_x_intervalo[media_intervalo] = 0
            min = max_intervalo

        # Genero diccionario de frecuencias por intervalo
        for variables_aleatorias in variables_aleatorias:
            for intervalo in intervalos:
                if intervalo.get("minimo") <= variables_aleatorias.get("aleatorio_decimal") < intervalo.get("maximo"):
                    frecuencias_x_intervalo[intervalo["media"]] += 1

        # Genero listas de medias, frecuencias observadas y esperadas a partir de datos anteriores
        frecuencia_esperada = round(len(numeros_aleatorios) / cantidad_intervalos, 4)
        if frecuencia_esperada == int(frecuencia_esperada):
            frecuencia_esperada = int(frecuencia_esperada)
        medias = [str(intervalo.get("media")).replace(".", ",") for intervalo in intervalos]
        frecuencias_obsevadas = list(frecuencias_x_intervalo.values())
        frecuencias_esperadas = [frecuencia_esperada] * len(intervalos)

        return medias, frecuencias_obsevadas, frecuencias_esperadas

    def generar_grafico_frecuencias(self, medias, frecuencias):

        sns.set_palette("deep",desat =.6)
        sns.set_context(rc={"figure.figsize":(8,4)})
        plt.hist(frecuencias, medias, edgecolor = 'black',  linewidth=1)
        plt.ylabel('frequencia')
        plt.title('Histograma')
        plt.show()

    def prueba_Chi_Cuadrado(self, frecuencias_observadas, frecuencias_esperadas):
        # Inicializo datos
        valores = [] * len(frecuencias_observadas)
        chi_cuadrado = 0

        # La funcion chisquare devuele en el primer campo el valor de chi cuadrado y en el segundo de p
        for i in range(len(frecuencias_esperadas)):
            aux = round(((frecuencias_observadas[i] - frecuencias_esperadas[i]) ** 2) / frecuencias_esperadas[i], 4)
            valores.append(aux)
        for valor in valores:
            chi_cuadrado += round(valor, 4)

        return chi_cuadrado

        #la distribucion debe ser un string como por ejemplo 'norm', para la normal 
    def prueba_Ktest(frecuencias_observadas,distribucion)
        stats.kstest(frecuencias_observadas,distrubicion)