class GeneradorCongruencial:

    semilla = None
    c = None
    a = None
    m = None

    def __init__(self, semilla=None, c=None, a=None, m=None):
        self.semilla = semilla
        if self.semilla is None:
            self.semilla = 37
        self.c = c
        if self.c is None:
            self.c = 43
        self.a = a
        if self.a is None:
            self.a = 13
        self.m = m
        if self.m is None:
            self.m = 101

    def generar_numero_aleatorio(self):
        aleatorio = round((self.c + self.a * self.semilla) % self.m, 4)
        self.semilla = aleatorio
        return aleatorio

