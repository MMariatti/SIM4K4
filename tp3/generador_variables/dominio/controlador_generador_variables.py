from matplotlib import pyplot
from scipy import stats
import numpy
import random
import math


class ControladorGeneradorVariables:
    
    def generar_variables_aleatorias_normal(self, mu, sigma, cantidad):

        # Convierto tipos de datos
        cantidad = int(cantidad)
        mu = float(mu.replace(",", "."))
        sigma = float(sigma.replace(",", "."))

        # Inicializo datos
        variables_aleatorias = []

        # Genero lista de variables aleatorias
        for i in range(0, cantidad):
            z = math.sqrt(-2 * math.log(1 - random.random())) * math.cos(2 * math.pi * random.random())
            va_normal = round(mu + z * sigma, 4)
            variables_aleatorias.append({
                "nro_orden": i + 1,
                "variable_aleatoria": va_normal
            })

        return variables_aleatorias

    def generar_variables_aleatorias_exponencial(self, lambd, cantidad):

        # Convierto tipos de datos
        cantidad = int(cantidad)
        lambd = float(lambd.replace(",", "."))

        # Inicializo datos
        variables_aleatorias = []

        # Genero lista de variables aleatorias
        for i in range(0, cantidad):
            va_exp = round(-1 / lambd * math.log(1 - random.random()), 4)
            variables_aleatorias.append({
                "nro_orden": i + 1,
                "variable_aleatoria": va_exp
            })

        return variables_aleatorias

    def generar_variables_aleatorias_poisson(self, lambd, cantidad):

        # Convierto tipos de datos
        cantidad = int(cantidad)
        lambd = float(lambd.replace(",", "."))

        # Inicializo datos
        variables_aleatorias = []

        # Genero lista de variables aleatorias
        variables_aleatorias_poisson = stats.poisson(lambd).rvs(size=cantidad)
        for i in range(0, cantidad):
            va_poisson = variables_aleatorias_poisson[i]
            variables_aleatorias.append({
                "nro_orden": i + 1,
                "variable_aleatoria": va_poisson
            })

        return variables_aleatorias

    def calcular_frecuencias_por_intervalo(self, variables_aleatorias, cantidad_intervalos, tipo_distribucion, mu=None,
                                           sigma=None, lambd=None):

        # Convierto tipos de datos
        cantidad_intervalos = int(cantidad_intervalos)
        if mu is not None:
            mu = float(mu.replace(",", "."))
            if mu == int(mu):
                mu = int(mu)
        if sigma is not None:
            sigma = float(sigma.replace(",", "."))
            if sigma == int(sigma):
                sigma = int(sigma)
        if lambd is not None:
            lambd = float(lambd.replace(",", "."))
            if lambd == int(lambd):
                lambd = int(lambd)

        # Inicializo datos
        lista_variables_aleatorias = [va.get("variable_aleatoria") for va in variables_aleatorias]
        minimo = min(lista_variables_aleatorias)
        maximo = max(lista_variables_aleatorias)
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
        for variable_aleatoria in lista_variables_aleatorias:
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
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.norm(mu, sigma).cdf(intervalo.get("maximo")) -
                                             stats.norm(mu, sigma).cdf(intervalo.get("minimo"))) *
                                            len(lista_variables_aleatorias), 2)
                if frecuencia_esperada == int(frecuencia_esperada):
                    frecuencia_esperada = int(frecuencia_esperada)
                frecuencias_esperadas.append(frecuencia_esperada)

        # Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion exponencial negativa
        elif tipo_distribucion == 1:
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.expon(0, 1 / lambd).cdf(intervalo.get("maximo")) -
                                             stats.expon(0, 1 / lambd).cdf(intervalo.get("minimo"))) *
                                            len(lista_variables_aleatorias), 2)
                if frecuencia_esperada == int(frecuencia_esperada):
                    frecuencia_esperada = int(frecuencia_esperada)
                frecuencias_esperadas.append(frecuencia_esperada)

        # Genero lista de frecuencias esperadas a partir de datos anteriores para distribucion de poisson
        elif tipo_distribucion == 2:
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.poisson(lambd).cdf(intervalo.get("maximo")) -
                                             stats.poisson(lambd).cdf(intervalo.get("minimo"))) *
                                            len(lista_variables_aleatorias), 2)
                if frecuencia_esperada == int(frecuencia_esperada):
                    frecuencia_esperada = int(frecuencia_esperada)
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

