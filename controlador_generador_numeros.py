from random import uniform

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from scipy.stats import chisquare



class ControladorGeneradorNumeros:

    def generar_numeros_congruente_mixo(self, cantidad, semilla, a, c, m):

        # Convierto tipos de datos
        cantidad = int(cantidad)
        semilla = round(float(semilla.replace(",", ".")), 4)
        a = round(float(a.replace(",", ".")), 4)
        c = round(float(c.replace(",", ".")), 4)
        m = round(float(m.replace(",", ".")), 4)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            aleatorio = round((a * semilla + c) % m, 4)
            aleatorio_decimal = round(aleatorio / m, 4)
            numeros_generados.append({
                "nro_orden": i + 1,
                "semilla": semilla,
                "aleatorio": aleatorio,
                "aleatorio_decimal": aleatorio_decimal
            })
            semilla = aleatorio

        return numeros_generados

    def generar_numeros_congruente_multiplicativo(self, cantidad, semilla, a, m):

        # Convierto tipos de datos
        cantidad = int(cantidad)
        semilla = round(float(semilla.replace(",", ".")), 4)
        a = round(float(a.replace(",", ".")), 4)
        m = round(float(m.replace(",", ".")), 4)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            aleatorio = round((a * semilla) % m, 4)
            aleatorio_decimal = round(aleatorio / m, 4)
            numeros_generados.append({
                "nro_orden": i + 1,
                "semilla": semilla,
                "aleatorio": aleatorio,
                "aleatorio_decimal": aleatorio_decimal
            })
            semilla = aleatorio

        return numeros_generados

    def generar_numeros_provisto_por_lenguaje(self, cantidad):

        # Convierto tipos de datos
        cantidad = int(cantidad)

        # Inicializo datos
        numeros_generados = []

        # Genero lista de numeros aleatorios
        for i in range(0, cantidad):
            aleatorio_decimal = round(uniform(0, 1), 4)
            numeros_generados.append({
                "nro_orden": i + 1,
                "aleatorio_decimal": aleatorio_decimal
            })

        return numeros_generados

    def generar_grafico_frecuencia(self, numeros_aleatorios, cantidad_intervalos):

        # Convierto tipos de datos
        cantidad_intervalos = int(cantidad_intervalos)

        # Inicializo datos
        min = 0
        max = 1
        paso = (max - min) / cantidad_intervalos
        intervalos = []
        frecuencias_x_intervalo = {}

        # Genero lista de intervalos e inicializo keys en diccionario de frecuencias por intervalo
        for i in range(0, cantidad_intervalos):
            min_intervalo = round(min, 4)
            max_intervalo = round(min_intervalo + paso, 4)
            media_intervalo = round(((min_intervalo + max_intervalo) / 2), 4)
            intervalos.append({
                "minimo": min_intervalo,
                "maximo": max_intervalo,
                "media": media_intervalo
            })
            frecuencias_x_intervalo[media_intervalo] = 0
            min = max_intervalo

        # Genero diccionario de frecuencias por intervalo
        for numero_aleatorio in numeros_aleatorios:
            for intervalo in intervalos:
                if intervalo.get("minimo") <= numero_aleatorio.get("aleatorio_decimal") < intervalo.get("maximo"):
                    frecuencias_x_intervalo[intervalo["media"]] += 1

        # Creo datasets para grafico
        frecuencias = ["Observada", "Esperada"]
        medias = [str(intervalo.get("media")).replace(".", ",") for intervalo in intervalos]
        frecuencia_esperada = round(len(numeros_aleatorios) / cantidad_intervalos, 4)
        datos = {
            "medias": medias,
            "Observada": list(frecuencias_x_intervalo.values()),
            "Esperada": [frecuencia_esperada] * len(intervalos)
        }

        # Genero grafico
        palette = ["#c9d9d3", "#718dbf", "#e84d60"]
        x = [(media, frecuencia) for media in medias for frecuencia in frecuencias]
        counts = sum(zip(datos["Observada"], datos["Esperada"]), ())
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        p = figure(x_range=FactorRange(*x), plot_height=350, title="Frecuencias observadas y esperadas",
                   toolbar_location=None, tools="")
        p.vbar(x="x", top="counts", width=0.9, source=source, line_color="white",
               fill_color=factor_cmap("x", palette=palette, factors=frecuencias, start=1, end=2))
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        show(p)


    # Metodo para obtener valor de chi de la serie de numeros aleatorios
 
    def prueba_chicuadrado(arrayFo, arrayFe,alpha,numeroIntervalos)
        grados_libertad = numeroIntervalos-1
        #chisquare devuele en el primer campo el valor de chi cuadrado y en el segundo de p
        valor_Prueba = chisquare(f_obs =arrayFo, f_exp=arrayFe, ddof=grados_libertad)
        #como lo que queremos comparar es el valor de chi en la variable valor_comparar metemos el valor del index = 0 de valor_prueba 
        # que es la variable que usamos para hacer el test.
        valor_Comparar = valor_Prueba[0]

	   
	   
	

