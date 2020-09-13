import numpy as np


class GeneradorNormal:

    mu = None
    sigma = None

    def __init__(self, mu=None, sigma=None):
        if mu is None:
            self.mu = 75
        if sigma is None:
            self.sigma = 15

    def generar_numero_aleatorio(self):
        return round(np.random.normal(self.mu, self.sigma), 4)
