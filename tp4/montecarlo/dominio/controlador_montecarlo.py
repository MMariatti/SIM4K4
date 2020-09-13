import math
from dominio.clases.generador_lenguaje import GeneradorLenguaje
from dominio.clases.generador_congruencial import GeneradorCongruencial
from dominio.clases.generador_normal import GeneradorNormal
from dominio.clases.generador_exponencial import GeneradorExponencial


class ControladorMontecarlo:

    def simular(self, parametros):

        # Obtengo parametros referidos al stock y convierto a tipos convenientes
        frascos_a_comprar = parametros.get("frascos_a_comprar")
        if frascos_a_comprar is not None:
            frascos_a_comprar = int(frascos_a_comprar)
        dias_cada_cuanto_comprar = parametros.get("dias_cada_cuanto_comprar")
        if dias_cada_cuanto_comprar is not None:
            dias_cada_cuanto_comprar = int(dias_cada_cuanto_comprar)
        peso_frasco = parametros.get("peso_frasco")
        if peso_frasco is not None:
            peso_frasco = int(peso_frasco)
        capacidad_maxima_frascos = parametros.get("capacidad_maxima_frascos")
        if capacidad_maxima_frascos is not None:
            capacidad_maxima_frascos = int(capacidad_maxima_frascos)

        # Obtengo parametros referidos a la demanda, convierto a tipos convenientes y creo objetos manejadores
        mu_normal = parametros.get("mu_normal")
        if mu_normal is not None:
            mu_normal = float(mu_normal.replace(",", "."))
        sigma_normal = parametros.get("sigma_normal")
        if sigma_normal is not None:
            sigma_normal = float(sigma_normal.replace(",", "."))
        mu_exponencial = parametros.get("mu_exponencial")
        if mu_exponencial is not None:
            mu_exponencial = float(mu_exponencial.replace(",", "."))
        generador_normal = GeneradorNormal(mu_normal, sigma_normal)
        generador_exponencial = GeneradorExponencial(mu_exponencial)

        # Obtengo parametros referidos a las horas por turno y convierto a tipos convenientes
        horas_maniana = parametros.get("horas_maniana")
        if horas_maniana is not None:
            horas_maniana = int(horas_maniana)
        horas_tarde = parametros.get("horas_tarde")
        if horas_tarde is not None:
            horas_tarde = int(horas_tarde)

        # Obtengo parametros referidos a la simulacion, convierto a tipos convenientes y creo objetos manejadores
        id_tipo_generador = parametros.get("id_tipo_generador")
        if id_tipo_generador is not None:
            id_tipo_generador = int(id_tipo_generador)
        dias = parametros.get("dias")
        if dias is not None:
            dias = int(dias)
        if id_tipo_generador == 0:
            generador_uniforme = GeneradorLenguaje()
        else:
            generador_uniforme = GeneradorCongruencial()

        # Inicializo lista para guardar vectores de estado
        dias_simulados = []

        # Inicializo variables iniciales
        demora = None
        frascos_disponibles = 0
        frascos_desechos = 0
        frascos_llegados = 0
        cafe_disponible = 0

        # Bucle principal
        for dia in range(1, dias + 1):

            # Aumento frascos disponibles o descuento dia de demora al iniciar el dia
            if demora is not None:
                if demora != 0:
                    demora -= 1
                if demora == 0:
                    demora = None
                    frascos_llegados = frascos_a_comprar
                    frascos_disponibles += frascos_llegados

            # Actualizo los gramos cafe disponible al iniciar el dia
            cafe_disponible += frascos_llegados * peso_frasco

            # Realizo pedido de compra de frascos si corresponde
            if dia - 1 % dias_cada_cuanto_comprar and demora is None:
                random_demora = generador_uniforme.generar_numero_aleatorio()
                if 0 <= random_demora < 0.5:
                    demora = 0
                elif 0.5 <= random_demora < 0.75:
                    demora = 1
                elif 0.75 <= random_demora < 1:
                    demora = 2

            # Consumo turno mañana

            # Comsumo turno tarde

            # Calculo Comsumo total
            consumo_total = 0

            # Actualizo los gramos cafe disponible al finalizar el dia
            cafe_disponible -= consumo_total

            # Calculo frascos disponibles al finalizar el dia
            frascos_disponibles = math.ceil(cafe_disponible / frascos_disponibles)

            # Desecho cafe si corresponde dependiendo capacidad máxima
            if frascos_disponibles > capacidad_maxima_frascos:
                frascos_desechos += frascos_disponibles - capacidad_maxima_frascos
                cafe_disponible = capacidad_maxima_frascos * peso_frasco
                frascos_disponibles = capacidad_maxima_frascos

        """
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
        """

        return [], {}

    """
    def simular_montecarlo(self, cantidad_dias, capacidad_maxima=10):

        demanda_manana = 0
        beneficio_manana = 0
        beneficio_tarde = 0
        faltante_manana = 0
        faltante_tarde = 0
        # demora = 0
        # frascos_regalados = 0
        # frascos_disponibles = 2

        faltante_total = 0
        simulacion_montecarlo = []* cantidad_dias

        for sim in range(len(simulacion_montecarlo)):

        # Planteo  condiciones de entrega y demora de pedidos

            # random_demora = round(random.random(), 4)

            # if sim % 2 == 0 and 0 <= random_demora < 0.5:
            #     demora = 0
            #     frascos_disponibles += 2
            # elif sim % 2 == 0 and 0.5 <= random_demora < 0.75:
            #     demora = 1
            # elif sim % 2 == 0 and 0.75 <= random_demora < 1:
            #     demora = 2
            #
            # elif sim % 2 != 0:
            #     random_demora = "X"
            #     demora = demora - 1
            #     if demora == 0:
            #         frascos_disponibles += 2
            #
            # if frascos_disponibles > capacidad_maxima:
            #     frascos_regalados += (frascos_disponibles-capacidad_maxima)
            #     frascos_disponibles = capacidad_maxima

            # cafe_disponible = frascos_disponibles*170

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
    """
