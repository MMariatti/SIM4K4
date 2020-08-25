from matplotlib import pyplot
from scipy import stats
import numpy
import statistics
import random
import math


class ControladorGeneradorVariables:
    
    def generar_variables_aleatorias_normal(self, mu, sigma, cantidad):

        # Inicializo datos
        variables_aleatorias = []

        # Genero lista de variables aleatorias
        for i in range(0, cantidad):
            z = math.sqrt(-2 * math.log(1 - random(0, 1))*math.cos(2 * math.pi * random(0, 1)))
            va_normal = round(mu + z * sigma, 4)
            variables_aleatorias.append(va_normal)

        return variables_aleatorias

    def generar_variables_aleatorias_exponencial(self, lamda, cantidad):

        # Inicializo datos
        variables_aleatorias = []

        # Genero lista de variables aleatorias
        for i in range(0, cantidad):
            va_exp = round((1 / lamda) * math.log(1 - random(0,1)), 4)
            variables_aleatorias.append(va_exp)

        return variables_aleatorias

    def generar_variables_aleatorias_poisson(self, lamda, cantidad):

        # Genero lista de variables aleatorias
        variables_aleatorias = numpy.random.poisson(lamda, cantidad)

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


        # Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion normal
        if tipo_distribucion == 0:
            media = statistics.mean(variables_aleatorias)
            desviacion_estandar = statistics.stdev(variables_aleatorias)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.norm(media, desviacion_estandar).cdf(intervalo.get("maximo")) -
                                             stats.norm(media, desviacion_estandar).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        # Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion exponencial negativa
        elif tipo_distribucion == 1:
            lambd = 1 / statistics.mean(variables_aleatorias)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.expon(0, 1 / lambd).cdf(intervalo.get("maximo")) -
                                             stats.expon(0, 1 / lambd).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        #Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion de poisson
        elif tipo_distribucion == 2:
            media = statistics.mean(variables_aleatorias)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.poisson(media).cdf(intervalo.get("maximo")) -
                                            stats.poisson(media).cdf(intervalo.get("minimo"))) *
            frecuencias_esperadas.append(frecuencia_esperada)

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

