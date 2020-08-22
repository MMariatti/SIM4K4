from random import uniform
import matplotlib.pyplot as plt
import numpy as np


class ControladorGeneradorNumeros:

    def generar_numeros_congruente_mixo(self, cantidad, semilla, a, c, m):

        # Convierto tipos de datos
        cantidad = int(cantidad)
        semilla = round(float(semilla.replace(",", ".")), 4)
        a = round(float(a.replace(",", ".")), 4)
        c = round(float(c.replace(",", ".")), 4)
        m = round(float(m.replace(",", ".")), 4)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            if i == 0:
                aleatorio = round(semilla % m, 4)
            else:
                aleatorio = round((a * semilla + c) % m, 4)
            aleatorio_decimal = round(aleatorio / m, 4)
            numeros_generados.append({
                "nro_orden": i + 1,
                "semilla": semilla,
                "aleatorio_decimal": aleatorio_decimal
            })
            semilla = aleatorio

        return numeros_generados

    def generar_numeros_congruente_multiplicativo(self, cantidad, semilla, a, m):

        # Convierto tipos de datos
        cantidad = int(cantidad)
        semilla = round(float(semilla.replace(",", ".")), 4)
        a = round(float(a.replace(",", ".")), 4)
        m = round(float(m.replace(",", ".")), 4)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            if i == 0:
                aleatorio = round(semilla % m, 4)
            else:
                aleatorio = round((a * semilla) % m, 4)
            aleatorio_decimal = round(aleatorio / m, 4)
            numeros_generados.append({
                "nro_orden": i + 1,
                "semilla": semilla,
                "aleatorio_decimal": aleatorio_decimal
            })
            semilla = aleatorio

        return numeros_generados

    def generar_numeros_provisto_por_lenguaje(self, cantidad):

        # Convierto tipos de datos
        cantidad = int(cantidad)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            aleatorio_decimal = round(uniform(0, 1), 4)
            numeros_generados.append({
                "nro_orden": i + 1,
                "aleatorio_decimal": aleatorio_decimal
            })

        return numeros_generados

    def calcular_frecuencias_por_intervalo(self, numeros_aleatorios, cantidad_intervalos):

        # Convierto tipos de datos
        cantidad_intervalos = int(cantidad_intervalos)

        # Inicializo datos
        min = 0
        max = 1
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
        for numero_aleatorio in numeros_aleatorios:
            for intervalo in intervalos:
                if intervalo.get("minimo") <= numero_aleatorio.get("aleatorio_decimal") < intervalo.get("maximo"):
                    frecuencias_x_intervalo[intervalo["media"]] += 1

        # Genero listas de medias, frecuencias observadas y esperadas a partir de datos anteriores
        frecuencia_esperada = round(len(numeros_aleatorios) / cantidad_intervalos, 4)
        if frecuencia_esperada == int(frecuencia_esperada):
            frecuencia_esperada = int(frecuencia_esperada)
        medias = [str(intervalo.get("media")).replace(".", ",") for intervalo in intervalos]
        frecuencias_obsevadas = list(frecuencias_x_intervalo.values())
        frecuencias_esperadas = [frecuencia_esperada] * len(intervalos)

        return medias, frecuencias_obsevadas, frecuencias_esperadas

    def prueba_chicuadrado(self, frecuencias_observadas, frecuencias_esperadas):

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

    def generar_grafico_frecuencias(self, medias, frecuencias_observadas, frecuencias_esperadas):

        # Creo grafico
        x = np.arange(len(medias))
        width = 0.35
        fig, ax = plt.subplots()
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
        plt.show()
