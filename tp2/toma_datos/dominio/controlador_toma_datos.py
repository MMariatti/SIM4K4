from matplotlib import pyplot
from scipy import stats
import numpy
import statistics
import xlrd


class ControladorTomaDatos:

    def obtener_variables_aleatorias(self, ruta_archivo, columna, fila_desde, fila_hasta):

        # Convierto tipos de datos y los adapto para usarlos con la libreria
        columna = int(columna) - 1
        fila_desde = int(fila_desde) - 1
        fila_hasta = int(fila_hasta) -1

        # Inicializo lista
        variables_aleatorias = []

        # Obtengo planilla
        archivo = xlrd.open_workbook(ruta_archivo)
        hoja = archivo.sheet_by_index(0)

        # Guardo valores en lista
        for i in range(fila_desde, fila_hasta + 1):
            valor = round(float(hoja.cell_value(i, columna)), 4)
            if valor == int(valor):
                valor = int(valor)
            variables_aleatorias.append(valor)

        return variables_aleatorias

    def calcular_frecuencias_por_intervalo(self, variables_aleatorias, cantidad_intervalos, tipo_distribucion):

        # Convierto tipos de datos
        cantidad_intervalos = int(cantidad_intervalos)

        # Inicializo datos
        minimo = min(variables_aleatorias)
        maximo = max(variables_aleatorias)
        paso = round(((maximo - minimo) / cantidad_intervalos), 2)
        intervalos = []
        frecuencias_x_intervalo = {}

        # Genero lista de intervalos e inicializo keys en diccionario de frecuencias por intervalo
        for i in range(0, cantidad_intervalos):
            min_intervalo = round(minimo, 2)
            if min_intervalo == int(min_intervalo):
                min_intervalo = int(min_intervalo)
            max_intervalo = round(min_intervalo + paso, 2)
            if max_intervalo == int(max_intervalo):
                max_intervalo = int(max_intervalo)
            media_intervalo = round(((min_intervalo + max_intervalo) / 2), 2)
            if media_intervalo == int(media_intervalo):
                media_intervalo = int(media_intervalo)
            intervalos.append({
                "minimo": min_intervalo,
                "maximo": max_intervalo,
                "media": media_intervalo
            })
            frecuencias_x_intervalo[media_intervalo] = 0
            minimo = max_intervalo

        # Genero diccionario de frecuencias por intervalo
        for variable_aleatoria in variables_aleatorias:
            for intervalo in intervalos:
                if intervalo.get("minimo") <= variable_aleatoria < intervalo.get("maximo"):
                    frecuencias_x_intervalo[intervalo.get("media")] += 1

        # Genero listas de medias y frecuencias observadas a partir de datos anteriores
        medias = [str(intervalo.get("media")).replace(".", ",") for intervalo in intervalos]
        frecuencias_obsevadas = list(frecuencias_x_intervalo.values())

        # Inicializo lista de frecuencias esperadas
        frecuencias_esperadas = []

        # Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion unifome
        if tipo_distribucion == 0:
            frecuencia_esperada = round(len(variables_aleatorias) / cantidad_intervalos, 2)
            if frecuencia_esperada == int(frecuencia_esperada):
                frecuencia_esperada = int(frecuencia_esperada)
            frecuencias_esperadas = [frecuencia_esperada] * len(intervalos)

        # Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion normal
        elif tipo_distribucion == 1:
            media = statistics.mean(variables_aleatorias)
            desviacion_estandar = statistics.stdev(variables_aleatorias)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.norm(media, desviacion_estandar).cdf(intervalo.get("maximo")) -
                                             stats.norm(media, desviacion_estandar).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        # Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion exponencial negativa
        elif tipo_distribucion == 2:
            media = statistics.mean(variables_aleatorias)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.expon(media).cdf(intervalo.get("maximo")) -
                                             stats.expon(media).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        return medias, frecuencias_obsevadas, frecuencias_esperadas

    def generar_histograma(self, medias, frecuencias_observadas):

        # Creo grafico
        y_pos = numpy.arange(len(medias))
        pyplot.bar(y_pos, frecuencias_observadas, align="center")
        pyplot.xticks(y_pos, medias)
        pyplot.ylabel("Frecuencias observadas")
        pyplot.title("Histograma")

        pyplot.show()
         
    def test_chi_cuadrado(self, frecuencias_observadas, frecuencias_esperadas):

        # Inicializo datos
        cantidad_intervalos = len(frecuencias_observadas)
        chi_cuadrado = 0

        # Calculo valor chi cuadrado
        for i in range(cantidad_intervalos):
            valor_intervalo = ((frecuencias_observadas[i] - frecuencias_esperadas[i]) ** 2) / frecuencias_esperadas[i] \
                if frecuencias_esperadas[i] != 0 else 0
            chi_cuadrado += valor_intervalo

        chi_cuadrado = round(chi_cuadrado, 2)
        if chi_cuadrado == int(chi_cuadrado):
            chi_cuadrado = int(chi_cuadrado)

        return chi_cuadrado

    def test_kolmogorov_smirnov(self, frecuencias_observadas, frecuencias_esperadas):

        # Inicializo datos
        cantidad_intervalos = len(frecuencias_observadas)
        probabilidad_frecuencias_observadas_acumulada = 0
        probabilidad_frecuencias_esperadas_acumulada = 0
        diferencias_probabilidades = []

        # Calculo valor kolmogorov-smirnov
        for i in range(cantidad_intervalos):
            probabilidad_frecuencias_observadas_acumulada += frecuencias_observadas[i] / cantidad_intervalos
            probabilidad_frecuencias_esperadas_acumulada += frecuencias_esperadas[i] / cantidad_intervalos

            valor_intervalo = round(abs(probabilidad_frecuencias_esperadas_acumulada -
                                        probabilidad_frecuencias_observadas_acumulada), 2)
            if valor_intervalo == int(valor_intervalo):
                valor_intervalo = int(valor_intervalo)
            diferencias_probabilidades.append(valor_intervalo)

        kolmogorov_smirnov = max(diferencias_probabilidades)

        return kolmogorov_smirnov
