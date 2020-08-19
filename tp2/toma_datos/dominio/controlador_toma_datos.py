from matplotlib import pyplot
from scipy import stats
import numpy
import statistics
import xlrd


class ControladorTomaDatos:

    def obtener_variables_aleatorias(self, ruta_archivo, columna, fila_desde, fila_hasta):

        # Convierto tipos de datos
        columna = int(columna)
        fila_desde = int(fila_desde)
        fila_hasta = int(fila_hasta)

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
                    frecuencias_x_intervalo[intervalo["media"]] += 1

        # Genero listas de medias y frecuencias observadas a partir de datos anteriores
        medias = [str(intervalo.get("media")).replace(".", ",") for intervalo in intervalos]
        frecuencias_obsevadas = list(frecuencias_x_intervalo.values())

        # Inicializo lista de frecuencias esperadas
        frecuencias_esperadas = []

        # Genero lista de frecuencias esperada a partir de datos anteriores para distribucion unifome
        if tipo_distribucion == 0:
            frecuencia_esperada = round(len(variables_aleatorias) / cantidad_intervalos, 2)
            if frecuencia_esperada == int(frecuencia_esperada):
                frecuencia_esperada = int(frecuencia_esperada)
            frecuencias_esperadas = [frecuencia_esperada] * len(intervalos)

        # Genero lista de frecuencias esperada a partir de datos anteriores para distribucion normal
        elif tipo_distribucion == 1:
            media = round(statistics.mean(variables_aleatorias), 2)
            desviacion_estandar = round(statistics.stdev(variables_aleatorias), 2)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.norm(media, desviacion_estandar).cdf(intervalo.get("maximo")) -
                                             stats.norm(media, desviacion_estandar).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        # Genero lista de frecuencias esperada a partir de datos anteriores para distribucion exponencial negativa
        elif tipo_distribucion == 2:
            frecuencias_esperadas = []

        return medias, frecuencias_obsevadas, frecuencias_esperadas

    def generar_grafico_frecuencias(self, medias, frecuencias_observadas, frecuencias_esperadas):

        # Creo grafico
        x = numpy.arange(len(medias))
        width = 0.35
        fig, ax = pyplot.subplots()
        rects1 = ax.bar(x - width / 2, frecuencias_observadas, width, label="Observadas")
        rects2 = ax.bar(x + width / 2, frecuencias_esperadas, width, label="Esperadas")

        ax.set_ylabel("Cantidad")
        ax.set_title("Frecuencias esperadas y observadas")
        ax.set_xticks(x)
        ax.set_xticklabels(medias)
        ax.legend()

        for rect in rects1:
            height = rect.get_height()
            ax.annotate("{}".format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                        textcoords="offset points", ha="center", va="bottom")
        for rect in rects2:
            height = rect.get_height()
            ax.annotate("{}".format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                        textcoords="offset points", ha="center", va="bottom")
        fig.tight_layout()
        pyplot.show()

    """
         
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
    
    """
