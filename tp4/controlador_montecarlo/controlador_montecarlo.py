import random 

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


	def simular_stock():
		pass
		