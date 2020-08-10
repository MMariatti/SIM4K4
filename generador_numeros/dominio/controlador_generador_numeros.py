from random import uniform


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
            aleatorio = round((a * semilla + c) % m, 4)
            aleatorio_decimal = round(aleatorio / m, 4)
            numeros_generados.append({
                "nro_orden": i+1,
                "semilla": semilla,
                "aleatorio": aleatorio,
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
            aleatorio = round((a * semilla) % m, 4)
            aleatorio_decimal = round(aleatorio / m, 4)
            numeros_generados.append({
                "nro_orden": i + 1,
                "semilla": semilla,
                "aleatorio": aleatorio,
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

    """
    def calcular_intervalos(self, cantidad):

        # Inicializo datos
        min = 0
        max = 1
        paso = max - min / cantidad
        intervalos = []
        media = []

        # Genero lista de intervalos
        for i in range(0, cantidad):


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
