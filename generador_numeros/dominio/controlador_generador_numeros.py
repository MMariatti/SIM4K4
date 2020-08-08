from decimal import Decimal


class ControladorGeneradorNumeros:

    def generador_congruente_mixo(self, cantidad, semilla, a, c, m):

        # Establezco constante para manejo de presicion de decimales
        FOURPLACES = Decimal(10) ** -4

        # Convierto parametros a tipos mas convenientes
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

    def generador_congruente_multiplicativo(self, cantidad, semilla, a, m):

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
