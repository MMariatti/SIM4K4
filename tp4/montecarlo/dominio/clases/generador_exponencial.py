import numpy as np


class GeneradorExponencial:

    mu = None

    def __init__(self, mu=None):
        self.mu = mu
        if self.mu is None:
            self.mu = 70

    def generar_numero_aleatorio(self):
        return round(np.random.exponential(self.mu), 4)
