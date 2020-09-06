from matplotlib import pyplot as plt
from scipy import stats
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
        cantidad_variables_aleatorias = len(lista_variables_aleatorias)
        minimo = min(lista_variables_aleatorias)
        maximo = max(lista_variables_aleatorias)
        paso = round(((maximo - minimo) / cantidad_intervalos), 2)
        intervalos = []
        frecuencias_observadas = []
        frecuencias_esperadas = []

        # Genero lista de intervalos
        for i in range(0, cantidad_intervalos):
            min_intervalo = round(minimo, 2)
            if min_intervalo == int(min_intervalo):
                min_intervalo = int(min_intervalo)
            max_intervalo = round(min_intervalo + paso, 2)
            if max_intervalo == int(max_intervalo):
                max_intervalo = int(max_intervalo)
            intervalos.append({
                "minimo": min_intervalo,
                "maximo": max_intervalo,
            })
            minimo = max_intervalo

        # Genero listas de frecuencias observadas y esperadas
        for intervalo in intervalos:
            minimo = intervalo.get("minimo")
            maximo = intervalo.get("maximo")

            # Calculo frecuencia observada de intervalo recorrido
            index_eliminar = []
            frecuencia_observada = 0
            for i in range(len(lista_variables_aleatorias) - 1, -1):
                variable_aleatoria = lista_variables_aleatorias[i]
                if minimo <= variable_aleatoria < maximo:
                    index_eliminar.append(i)
                    frecuencia_observada += 1
            for i in index_eliminar:
                del lista_variables_aleatorias[i]
            frecuencias_observadas.append(frecuencia_observada)

            # Calculo frecuencia esperada de intervalo recorrido segun tipo de distribucion
            frecuencia_esperada = 0
            if tipo_distribucion == 0:
                frecuencia_esperada = round((stats.norm(mu, sigma).cdf(maximo) -
                                             stats.norm(mu, sigma).cdf(minimo)) *
                                            cantidad_variables_aleatorias, 2)
            elif tipo_distribucion == 1:
                frecuencia_esperada = round((stats.expon(0, 1 / lambd).cdf(maximo) -
                                             stats.expon(0, 1 / lambd).cdf(minimo)) *
                                            cantidad_variables_aleatorias, 2)
            elif tipo_distribucion == 2:
                frecuencia_esperada = round((stats.poisson(lambd).cdf(maximo) -
                                             stats.poisson(lambd).cdf(minimo)) *
                                            cantidad_variables_aleatorias, 2)
            if frecuencia_esperada == int(frecuencia_esperada):
                frecuencia_esperada = int(frecuencia_esperada)
            frecuencias_esperadas.append(frecuencia_esperada)

        return frecuencias_observadas, frecuencias_esperadas

    def generar_grafico_frecuencias(self, variables_aleatorias, cantidad_intervalos):

        # Preparo datos para grafico
        datos = [va.get("variable_aleatoria") for va in variables_aleatorias]
        bins = int(cantidad_intervalos)

        # Creo grafico
        plt.hist(datos, bins, histtype="bar", rwidth=0.8)
        plt.title("Variables aleatorias observadas")
        plt.xlabel("Variables aleatorias")
        plt.ylabel("Cantidad")
        plt.show()

    def test_chi_cuadrado(self, frecuencias_observadas, frecuencias_esperadas, alpha):

        # Inicializo datos
        cantidad_intervalos = len(frecuencias_observadas)
        chi_cuadrado = 0

        # Calculo valor chi cuadrado de la muestra
        for i in range(cantidad_intervalos):
            valor_intervalo = ((frecuencias_observadas[i] - frecuencias_esperadas[i]) ** 2) / frecuencias_esperadas[i] \
                if frecuencias_esperadas[i] != 0 else 0
            chi_cuadrado += valor_intervalo
        chi_cuadrado = round(chi_cuadrado, 4)
        if chi_cuadrado == int(chi_cuadrado):
            chi_cuadrado = int(chi_cuadrado)

        # Obtengo valor chi cuadrado de tabla
        grados_libertad = cantidad_intervalos - 1
        chi_cuadrado_tabla = round(stats.chi2.isf(alpha, grados_libertad), 4)
        if chi_cuadrado_tabla == int(chi_cuadrado_tabla):
            chi_cuadrado_tabla = int(chi_cuadrado_tabla)

        return chi_cuadrado, chi_cuadrado_tabla
