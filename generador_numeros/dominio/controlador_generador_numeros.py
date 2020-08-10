from decimal import Decimal
from random import uniform


class ControladorGeneradorNumeros:

    def generar_numeros_congruente_mixo(self, cantidad, semilla, a, c, m):

        # Establezco constante para manejo de presicion de decimales
        FOURPLACES = Decimal(10) ** -4

        # Convierto parametros a tipos convenientes
        cantidad = int(cantidad)
        semilla = Decimal(semilla).quantize(FOURPLACES)
        a = Decimal(a).quantize(FOURPLACES)
        c = Decimal(c).quantize(FOURPLACES)
        m = Decimal(m).quantize(FOURPLACES)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            aleatorio = Decimal((a * semilla + c) % m).quantize(FOURPLACES)
            aleatorio_decimal = Decimal(aleatorio / m).quantize(FOURPLACES)
            numeros_generados.append({
                "nro_orden": i+1,
                "semilla": semilla,
                "aleatorio": aleatorio,
                "aleatorio_decimal": aleatorio_decimal
            })
            semilla = aleatorio

        return numeros_generados

    def generar_numeros_congruente_multiplicativo(self, cantidad, semilla, a, m):

        # Establezco constante para manejo de presicion de decimales
        FOURPLACES = Decimal(10) ** -4

        # Convierto parametros a tipos mas convenientes
        cantidad = int(cantidad)
        semilla = Decimal(semilla).quantize(FOURPLACES)
        a = Decimal(a).quantize(FOURPLACES)
        m = Decimal(m).quantize(FOURPLACES)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            aleatorio = Decimal((a * semilla) % m).quantize(FOURPLACES)
            aleatorio_decimal = Decimal(aleatorio / m).quantize(FOURPLACES)
            numeros_generados.append({
                "nro_orden": i + 1,
                "semilla": semilla,
                "aleatorio": aleatorio,
                "aleatorio_decimal": aleatorio_decimal
            })
            semilla = aleatorio

        return numeros_generados

    def generar_numeros_provisto_por_lenguaje(self, cantidad):

        # Establezco constante para manejo de presicion de decimales
        FOURPLACES = Decimal(10) ** -4

        # Convierto parametros a tipos mas convenientes
        cantidad = int(cantidad)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            aleatorio_decimal = Decimal(uniform(0, 1)).quantize(FOURPLACES)
            numeros_generados.append({
                "nro_orden": i + 1,
                "aleatorio_decimal": aleatorio_decimal
            })

        return numeros_generados

    """
    def calcular_intervalos(self, cantidad_intervalos):

        # Inicializo datos
        min = 0
        max = 1
        paso = max - min / cantidad_intervalos
        intervalos = []
        media = []
        i = 0

        # Genero lista con intervalos
        while i < cantidad_Intervalos :
        # el array de intervalos, termina siendo una matriz, ya que en la primer columna se guarda el valor de piso del 
        intevalo y en la segunda se guarda el valor de techo del intervalo
            if i == 0:
                intervalos.append([round(minimo,4),round(minimo + paso, 4)] )
            else:
                ultimoMinimo = round(intervalos[i-1][1],4)
                intervalos.append([ultimoMinimo,round(ultimoMinimo+paso,4)])

            i=+1

        for i in intervalos:
            media.append(round((i[0] + i[1]) / 2, 4))

        return intervalos, media
    """
