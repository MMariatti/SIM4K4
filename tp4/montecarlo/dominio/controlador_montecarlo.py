import random 
import numpy as np


class ControladorMontecarlo:

    def simular(self, parametros):

        dias_simulados = []
        for i in range(1, 10001):
            dias_simulados.append({
                "nro_dia": i,
                "stock": i,
                "cafe_almacenado_promedio": i,
                "cafe_faltante_promedio": i,
                "ingreso": i,
                "ingreso_promedio": i,
                "contribucion": i,
                "contribucion_promedio": i
            })

        resultados = {
            "porcentaje_dias_faltantes": 10,
            "porcentaje_dias_0_a_2_frascos": 20,
            "porcentaje_dias_2_a_5_frascos": 30,
            "porcentaje_dias_5_a_8_frascos": 50,
            "porcentaje_dias_mas_8_frascos": 60,
            "promedio_horas_perdidas": 70,
            "tiene_stock": True
        }

        return dias_simulados, resultados

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

        def simular_montecarlo(cantidad_dias, capacidad_maxima=10):

        demanda_manana = 0
        beneficio_manana = 0
        beneficio_tarde = 0
        faltante_manana = 0
        faltante_tarde = 0
        demora = 0
        frascos_regalados = 0
        frascos_disponibles = 2

        faltante_total = 0
        simulacion_montecarlo = []* cantidad_dias

        for sim in range(len(simulacion_montecarlo)):

        # Planteo  condiciones de entrega y demora de pedidos

            random_demora = round(random.random(), 4)

            if sim % 2 == 0 and 0 <= random_demora < 0.5:
                demora = 0
                frascos_disponibles += 2
            elif sim % 2 == 0 and 0.5 <= random_demora < 0.75:
                demora = 1
            elif sim % 2 == 0 and 0.75 <= random_demora < 1:
                demora = 2

            elif sim % 2 != 0:
                random_demora = "X"
                demora = demora - 1
                if demora == 0:
                    frascos_disponibles += 2

            if frascos_disponibles > capacidad_maxima:
                frascos_regalados += (frascos_disponibles-capacidad_maxima)
                frascos_disponibles = capacidad_maxima

            cafe_disponible = frascos_disponibles*170

            # Planteo condiciones del turno mañana

            random_manana = round(random.random(), 4)
            if random_manana < 0.5:

                demanda_manana = 50

            elif 0.5 <= random_manana < 1:

                demanda_manana = round(random.normalvariate(75, 15), 4)

            if demanda_manana <= cafe_disponible:

                beneficio_manana = round((demanda_manana * 15), 4)
                cafe_disponible = cafe_disponible-demanda_manana

            elif demanda_manana > cafe_disponible:

                beneficio_manana = round((cafe_disponible*15), 4)
                faltante_manana = round((demanda_manana-cafe_disponible), 4)
                cafe_disponible = 0

            # Planteo condiciones del turno tarde

            demanda_tarde = round(np.random.exponential(79), 0)

            if demanda_tarde <= cafe_disponible:

                beneficio_tarde = round((demanda_tarde*15), 4)
                cafe_disponible = round((cafe_disponible-demanda_tarde), 4)

            elif demanda_tarde > cafe_disponible:
                beneficio_tarde = round((cafe_disponible*15), 4)
                faltante_tarde = round((demanda_tarde-cafe_disponible), 4)
                cafe_disponible = 0

            if cafe_disponible == 0:
                beneficio_tarde = 0

            demanda_total = round((demanda_manana + demanda_tarde), 4)

            faltante_total = round((faltante_manana+faltante_tarde), 4)

            beneficio_total = round((beneficio_manana + beneficio_tarde), 4)

            simulacion_montecarlo.append({"Dia":sim+1,
                                          "Random demora":random_demora,
                                          "Demora":demora,
                                          "Frascos disponibles":frascos_disponibles,
                                          "Random mañana":random_manana,
                                          "Mañana":demanda_manana,
                                          "Beneficio mañana":beneficio_manana,
                                          "Faltante mañana":faltante_manana
                                          "Tarde":demanda_tarde,
                                          "Beneficio tarde":beneficio_tarde
                                          "Faltante tarde":faltante_tarde,
                                          "Beneficio":beneficio_total
                                          "Faltante":faltante_total,
                                          "Frascos regalados":frascos_regalados
                                        })
