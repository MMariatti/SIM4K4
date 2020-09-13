class GeneradorCongruencial:

    semilla = None
    c = None
    a = None
    m = None

    def __init__(self, semilla=None, c=None, a=None, m=None):
        if semilla is None:
            self.semilla = 37
        if c is None:
            self.c = 43
        if a is None:
            self.a = 13
        if m is None:
            self.m = 101

    def generar_numero_aleatorio(self):
        aleatorio = round((self.c + self.a * self.semilla) % self.m, 4)
        self.semilla = aleatorio
        return aleatorio

