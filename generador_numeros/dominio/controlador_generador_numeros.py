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
                "nro_orden": i + 1,
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

    def calcular_intervalos(self, cantidad):

        # Convierto tipos de datos
        cantidad = int(cantidad)

        # Inicializo datos
        min = 0
        max = 1
        paso = (max - min) / cantidad
        intervalos = []

        # Genero lista de intervalos
        for i in range(0, cantidad):
            min_intervalo = round(min, 4)
            max_intervalo = round(min_intervalo + paso, 4)
            media_intervalo = round(((min_intervalo + max_intervalo) / 2), 4)
            intervalos.append({
                "nro_intervalo": i + 1,
                "minimo": min_intervalo,
                "maximo": max_intervalo,
                "media": media_intervalo,
            })
            min = max_intervalo

        return intervalos
