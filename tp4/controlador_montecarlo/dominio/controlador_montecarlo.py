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
		demanda = 0
		random_entrega_pedido = round(random(0,1),4)
		frascos_disponibles = 2
		turno = ""

		simulacion_stock = []*cantidad_dias

		for i in range(0, cantidad_dias):

			if (random_turno < 0,5):
				turno = "Mañana"
			elif(random_turno > 0,5):
				turno = "Tarde"

			if(turno == "Mañana" and random_demanda < 0,5):
				demanda = 50
			elif (turno == "Mañana" and random_demanda < 0,5):
				demanda = np.random.normal(75,15,1)

			elif (turno =="Tarde" and random_demanda < 0,5):
				demanda = np.random.exponential(79, size = 1)

			if(demanda <= frascos_disponibles*170):
				beneficio = demanda*precio_venta
				faltante = 0
			elif(demanda > frascos_disponibles*170):
				beneficio = frascos_disponibles*precio_venta
				faltante = (demanda-(frascos_disponibles*170))*costo_faltante

			simulacion_stock.append({"Dia":i+1,"Turno":turno,"demanda":demanda,"beneficio":beneficio,"faltante":faltante})

		return simulacion_stock

			
		