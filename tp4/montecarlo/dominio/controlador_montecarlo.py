import random 
import numpy as np


class ControladorMontecarlo:

    def elegir_modo_aleatorios(self, tipo_aleatorio, cantidad=None, semilla=None, a=None, c=None, m=None):
        numero_aleatorio = None

        if tipo_aleatorio == 0:
            numero_aleatorio = round(random.random(), 4)

        elif tipo_aleatorio == 1:
            cantidad = int(cantidad)
            semilla = round(float(semilla.replace(",", ".")), 4)
            a = round(float(a.replace(",", ".")), 4)
            c = round(float(c.replace(",", ".")), 4)
            m = round(float(m.replace(",", ".")), 4)

            # Inicializo datos
            numero_aleatorio = []

            # Genero lista de numeros aleatorios
            for i in range(0, cantidad):
                if i == 0:
                    aleatorio = round(semilla % m, 4)
                else:
                    aleatorio = round((a * semilla + c) % m, 4)
                aleatorio_decimal = round(aleatorio / m, 4)
                numero_aleatorio.append({
                    "nro_orden": i + 1,
                    "semilla": semilla,
                    "aleatorio_decimal": aleatorio_decimal
                })
                semilla = aleatorio

        return numero_aleatorio

    def simular_stock(self, cantidad_dias, capacidad_maxima=10):
        # Pongo que el costo de venta es 15 xq resulta de dividir $150 en 100gr
        precio_venta = 15

        # Pongo que el costo del faltante es 10 xq resulta de dividir $100 en 100gr
        costo_faltante = 10

        costo_frasco = 250

        random_demanda_m = round(random.random(), 4)
        random_demanda_t = round(random.random(), 4)
        demanda_manana = 0
        demanda_tarde = 0
        random_entrega_pedido = round(random.random(), 4)
        frascos_disponibles = 2
        cafe_disponible = frascos_disponibles*170

        simulacion_stock = []*cantidad_dias

        for i in range(0, cantidad_dias):

            string_m = "Mañana"

            if string_m == "Mañana" and (0 <= random_demanda_m < 0.5):
                demanda_manana = 50

            elif string_m == "Mañana" and (0.5 <= random_demanda_m < 1):
                demanda_manana = round(random.normalvariate(75, 15), 0)

            if demanda_manana <= cafe_disponible:
                beneficio_manana = demanda_manana*precio_venta
                faltante_manana = 0
                faltante_manana = cafe_disponible-demanda_manana

            elif demanda_manana > cafe_disponible:
                beneficio_manana = demanda_manana*precio_venta
                faltante_manana = (demanda_manana - cafe_disponible) * costo_faltante
                cafe_disponible = 0

            string_t = "Tarde"

            if string_t == "Tarde":
                demanda_tarde = round(np.random.exponential(79), 0)

            if demanda_tarde <= cafe_disponible:
                beneficio_tarde = demanda_tarde * precio_venta
                faltante_tarde = 0
                cafe_disponible = cafe_disponible - demanda_tarde

            elif demanda_tarde > frascos_disponibles*170:
                beneficio_tarde = demanda_tarde * precio_venta
                faltante_tarde = (demanda_tarde - cafe_disponible) * costo_faltante
                cafe_disponible = 0

            beneficio_total = beneficio_manana + beneficio_tarde
            faltante_total = faltante_manana + faltante_tarde

            simulacion_stock.append({"Dia": i+1,
                                     "Random": random_demanda_m,
                                     "Mañana": demanda_manana,
                                     "Faltante mañana": faltante_manana,
                                     "Tarde": beneficio_tarde,
                                     "Faltante Tarde": faltante_tarde,
                                     "Beneficio total": beneficio_total,
                                     "Faltante total": faltante_total,
                                     "Cafe disponible": cafe_disponible})

            return simulacion_stock
