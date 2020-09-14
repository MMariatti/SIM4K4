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
        frascos_llegados = 0
        frascos_disponibles = 0
        frascos_desechos = 0
        cafe_disponible = 0

        # Bucle principal
        for dia in range(1, dias + 1):

            # Actualizo frascos disponibles o descuento dia de demora al iniciar el dia
            costo = 0
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
            demanda_abastecida = 0
            demanda_no_abastecida = 0
            if demanda <= cafe_disponible:
                demanda_abastecida = demanda
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
                frascos_desechos += frascos_disponibles - capacidad_maxima_frascos
                cafe_disponible = capacidad_maxima_frascos * peso_frasco
                frascos_disponibles = capacidad_maxima_frascos

            # Agrego vector de estado a lista
            dias_simulados.append({
                "nro_dia": dia,
                "dia_compra": dia_compra,
                "demora": demora,
                "frascos_disponibles": frascos_disponibles,
                "cafe_disponible": cafe_disponible,
                # "cafe_disponible_promedio": cafe_disponible_promedio,
                "demanda": demanda,
                "demanda_no_abastecida": demanda_no_abastecida,
                # "demanda_no_abastecida_promedio": demanda_no_abastecida_promedio,
                "ingreso": ingreso,
                # "ingreso_promedio": ingreso_promedio,
                "beneficio": beneficio,
                # "beneficio_promedio": beneficio_promedio
            })

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
