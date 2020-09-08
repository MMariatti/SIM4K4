import random 
import numpy as np

class controlador_montecarlo:
	
	def elegir_modo_aleatorios(tipoAleatorio):
		if tipoAleatorio == 0:
			numeroAleatorio = round(random(0,1),4)

		elif tipoAleatorio == 1:
			 cantidad = int(cantidad)
	        semilla = round(float(semilla.replace(",", ".")), 4)
	        a = round(float(a.replace(",", ".")), 4)
	        c = round(float(c.replace(",", ".")), 4)
	        m = round(float(m.replace(",", ".")), 4)

	        # Inicializo datos
	        numeroAleatorio = []

	        # Genero lista de numeros aleatorios
	        for i in range(0, cantidad):
	            if i == 0:
	                aleatorio = round(semilla % m, 4)
	            else:
	                aleatorio = round((a * semilla + c) % m, 4)
	            aleatorio_decimal = round(aleatorio / m, 4)
	            numeroAleatorio.append({
	                "nro_orden": i + 1,
	                "semilla": semilla,
	                "aleatorio_decimal": aleatorio_decimal
	            })
	            semilla = aleatorio

	    return numeroAleatorio


	def simular_stock(cantidad_dias,capacidad_maxima=10):
            #Pongo que el costo de venta es 15 xq resulta de dividir $150 en 100gr
            precio_venta = 15
            #Pongo que el costo del faltante es 10 xq resulta de dividir $100 en 100gr
            costo_faltante = 10

            costo_frasco= 250

            random_demandaM = round(random.random(),4)
            random_demandaT = round(random.random(),4)
            demandaManana = 0
            demandaTarde = 0
            random_entrega_pedido = round(random.random(),4)
            frascos_disponibles = 2
            cafe_disponible = frascos_disponibles*170

            simulacion_stock = []*cantidad_dias

            for i in range(0, cantidad_dias):

                stringM = "Mañana"

                if stringM == "Mañana" and (0 <= random_demandaM < 0.5):
                    demandaManana = 50

                elif stringM == "Mañana" and (0.5 <= random_demandaM < 1):
                    demandaManana = round(random.normalvariate(75,15),0)


                if demandaManana <= cafe_disponible:
                    beneficioManana = demandaManana*precio_venta
                    faltanteManana = 0
                    cafe_disponible = cafe_disponible-demandaManana

                elif demandaManana > cafe_disponible:
                    beneficioManana = demandaManana*precio_venta
                    faltanteManana  = (demandaManana-(cafe_disponible))*costo_faltante
                    cafe_disponible = 0


                stringT = "Tarde"

                if stringT =="Tarde":
                    demandaTarde = round(np.random.exponential(79),0)

                if demandaTarde <= cafe_disponible:
                    beneficioTarde = demandaTarde*precio_venta
                    faltanteTarde = 0
                    cafe_disponible = cafe_disponible-demandaTarde

                elif demandaTarde > frascos_disponibles*170:
                    beneficioTarde = demandaTarde*precio_venta
                    faltanteTarde = (demandaTarde-cafe_disponible)*costo_faltante
                    cafe_disponible = 0

                beneficioTotal = beneficioManana + beneficioTarde
                faltanteTotal = faltanteManana+faltanteTarde




                simulacion_stock.append({"Dia":i+1,"Random":random_demandaM,"Mañana":demandaManana,"Faltante mañana":faltanteManana,

                    "Tarde":beneficioTarde,"faltante Tarde":faltanteTarde, "Beneficio total":beneficioTotal,
                                         "Faltante total":faltanteTotal,"Cafe disponible":cafe_disponible})

                return simulacion_stock