class ControladorGeneradorNumeros:

    def generador_congruente_mixo(self, cantidad, semilla, a, c, m):
        numeros_generados = [None] * cantidad
        index = 0
        for i in range(0, cantidad):
            if index != 0:
                semilla = (c* semilla + a) % m
            numeros_generados[i] = semilla / m
            index += 1
        return numeros_generados

    def generador_congruente_multiplicativo(self, cantidad, semilla, a, m):
        numeros_generados = [None] * cantidad
        index = 0
        for i in range(0, cantidad):
            if index != 0:
                semilla = (c * semilla) % m
            numeros_generados[i] = semilla / m
            index += 1
        return numeros_generados
