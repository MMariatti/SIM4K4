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

		random_turno = round(random(0,1),4)
		random_demanda = round(random(0,1),4)
		demandaManana = 0
		demandaTarde = 0
		random_entrega_pedido = round(random(0,1),4)
		frascos_disponibles = 2
		

		simulacion_stock = []*cantidad_dias

		for i in range(0, cantidad_dias):

			turno = "Mañana"

			if(turno == "Mañana" and random_demanda < 0,5):
				demanda = 50
			elif (turno == "Mañana" and random_demanda < 0,5):
				demandaManana = np.random.normal(75,15,1)

			if (demandaManana <= frascos_disponibles*170):
				beneficioManana = demandaManana*precio_venta
				faltanteManana = 0
			elif(demandaManana > frascos_disponibles*170):
				beneficioManana = demandaManana*precio_venta
				faltanteManana  = (demanda-(frascos_disponibles*170))*costo_faltante

			turno = "Tarde"

			elif (turno =="Tarde"):
				demandaTarde = np.random.exponential(79, size = 1)

			if(demandaTarde <= frascos_disponibles*170):
				beneficioTarde = demanda*precio_venta
				faltanteTarde = 0
			elif(demandaTarde > frascos_disponibles*170):
				beneficio = demandaTarde*precio_venta
				faltante = (demandaTarde-(frascos_disponibles*170))*costo_faltante

			beneficioTotal = beneficioManana + beneficioTarde
			faltanteTotal = faltanteManana+faltanteTarde

			simulacion_stock.append({"Dia":i+1,"Mañana":demandaManana,"Faltante mañana":faltanteManana,
				"Tarde":beneficioTarde,"faltante Tarde":faltante, "Beneficio total":beneficioTotal,"Faltante total":faltanteTotal})

		return simulacion_stock

			
		