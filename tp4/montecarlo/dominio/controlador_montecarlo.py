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

        # Inicializo variables iniciales que se usaran durante el algoritmo
        demora = 0
        frascos_disponibles = 0
        cafe_disponible = 0

        # Inicializo vector de estado del dia cero y lista para guardar vectores de estado anteriores
        dia_simulado = {}
        dias_simulados = []

        # Inicializo vector de estado para dia cero
        dia_simulado["nro_dia"] = 0
        dia_simulado["dia_compra"] = False
        dia_simulado["demora"] = None
        dia_simulado["frascos_disponibles"] = 0
        dia_simulado["cafe_disponible"] = 0
        dia_simulado["cafe_disponible_promedio"] = 0
        dia_simulado["demanda"] = 0
        dia_simulado["demanda_no_abastecida"] = 0
        dia_simulado["demanda_no_abastecida_promedio"] = 0
        dia_simulado["ingreso"] = 0
        dia_simulado["ingreso_promedio"] = 0
        dia_simulado["beneficio"] = 0
        dia_simulado["beneficio_promedio"] = 0

        # Bucle principal
        for dia in range(1, dias + 1):

            # Inicializo vector de estado del dia anterior y limpio el del dia actual antes de comenzar con los calculos
            dia_anterior_simulado = dia_simulado
            dia_simulado = {}

            # CALCULOS PARA EL DIA ACTUAL

            # Actualizo frascos disponibles o descuento dia de demora al iniciar el dia
            costo = 0
            frascos_llegados = 0
            if demora is not None:
                if demora != 0:
                    demora -= 1
                if demora == 0:
                    demora = None
                    costo = frascos_a_comprar * 250
                    frascos_llegados = frascos_a_comprar
                    frascos_disponibles += frascos_llegados

            # Actualizo los gramos cafe disponible al iniciar el dia
            cafe_disponible += frascos_llegados * peso_frasco

            # Realizo pedido de compra de frascos si corresponde
            dia_compra = (dia - 1 % dias_cada_cuanto_comprar and demora is None)
            if dia_compra:
                random_demora = generador_uniforme.generar_numero_aleatorio()
                if 0 <= random_demora < 0.5:
                    demora = 0
                elif 0.5 <= random_demora < 0.75:
                    demora = 1
                elif 0.75 <= random_demora < 1:
                    demora = 2

            # Demanda diaria
            random_maniana = generador_uniforme.generar_numero_aleatorio()
            if 0 <= random_maniana < 0.5:
                demanda_maniana = 50
            else:
                demanda_maniana = generador_normal.generar_numero_aleatorio()
            demanda_tarde = generador_exponencial.generar_numero_aleatorio()
            demanda = demanda_maniana + demanda_tarde

            # Calculo la demanda abastecida y no abastecida y actualizo los gramos de cafe disponibles al finalizar
            # el dia
            if demanda <= cafe_disponible:
                demanda_abastecida = demanda
                demanda_no_abastecida = 0
                cafe_disponible -= demanda
            else:
                demanda_abastecida = cafe_disponible
                demanda_no_abastecida = demanda - cafe_disponible
                cafe_disponible = 0

            # Ingreso diario
            ingreso = demanda_abastecida * 1.5

            # Beneficio diario
            beneficio = ingreso - costo

            # Actualizo los frascos disponibles al finalizar el dia
            frascos_disponibles = math.ceil(cafe_disponible / frascos_disponibles)

            # Desecho cafe si corresponde dependiendo capacidad máxima
            if frascos_disponibles > capacidad_maxima_frascos:
                # frascos_desechos += frascos_disponibles - capacidad_maxima_frascos
                cafe_disponible = capacidad_maxima_frascos * peso_frasco
                frascos_disponibles = capacidad_maxima_frascos

            # Gurdo datos en vector de estado del dia actual

            dia_simulado["nro_dia"] = dia
            dia_simulado["dia_compra"] = dia_compra
            dia_simulado["demora"] = demora
            dia_simulado["frascos_disponibles"] = frascos_disponibles
            dia_simulado["cafe_disponible"] = cafe_disponible
            # dia_simulado["cafe_disponible_promedio"] = cafe_disponible_promedio
            dia_simulado["demanda"] = demanda
            dia_simulado["demanda_no_abastecida"] = demanda_no_abastecida
            # dia_simulado["demanda_no_abastecida_promedio"] = demanda_no_abastecida_promedio
            dia_simulado["ingreso"] = ingreso
            # dia_simulado["ingreso_promedio"] = ingreso_promedio
            dia_simulado["beneficio"] = beneficio
            # dia_simulado["beneficio_promedio"] = beneficio_promedio

            # Agrego vector de estado a lista
            dias_simulados.append(dia_simulado)

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
