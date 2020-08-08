import sys
from PyQt5.QtWidgets import QApplication
from interfaz.ventana_generador_numeros import VentanaGeneradorNumeros


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VentanaGeneradorNumeros()
    window.show()
    app.exec_()
    
    semilla = int(VentanaGeneradorNumeros.TxtSemillaValue)
    a = int(VentanaGeneradorNumeros.TxtConstanteAValue)
    c = int(VentanaGeneradorNumeros.TxtConstanteCValue)
    m = int(VentanaGeneradorNumeros.TxtConstanteMVAlue)
    numeros = int(VentanaGeneradorNumeros.TxtConstanteMValue)

    lista = ControladorGeneradorNumeros.generador_congruente_mixto(numeros, semilla, a, c, m)


