from matplotlib import pyplot
from scipy import stats
import numpy
import statistics
import xlrd
import random
import math

class ControladorGeneradorVA:
    
    def generar_VA_Normal(self,mu,sigma,cantidad):
        #defino las listas de aleatorios y la de z
        """
        array_aleatorio1 = []*cantidad
        array_aleatorio2 = []*cantidad
        array_z =[]*cantidad
        """
        array_VA_Normal = []*cantidad
        """
        #Lleno la primer lista de aleatorios
        for i in range(len(array_aleatorio1)):
           aleatorio = round(random(0,1),4)
           array_aleatorio1.append(aleatorio)

        #Creo la segunda lista de aleatorios
        for i in range(array_aleatorio2):
           aleatorio = round(random(0,1),4)
           array_aleatorio2.append(aleatorio)

        #Creo la lista de valores z con la formula z=sqrt(2*ln(1-random1)*cos(2pi*random2))
        for i in range(len(array_z)):
            z =sqrt(-2*math.log(1-array_aleatorio1[i]*cos(2*math.pi*array_aleatorio2[i])))
            array_z.append(z)
        """
        #Finalmente lleno la lista de variables aleatorias

        for i in range(len(array_VA)):
            z = sqrt(-2*math.log(1-round(random(0,1)))*cos(2*math.pi*round(random(0,1))))
            va_normal = round(mu+z*sigma,4)
            array_VA_Normal.append(va_normal)

        return array_VA_Normal

    def generar_VA_exponencial(self,lamda,cantidad):
        
        array_VA_exponencial= []*cantidad
        for i in range(len(array_VA)):
            va_exp =round((1/lamda)*math.log(1-round(random(0,1),4)),4)
            array_VA_exponencial.append(va_exp)

        return array_VA_exponencial

    def generar_VA_poisson(self,lamda,cantidad):

        array_VA_poisson = numpy.random.poisson(lamda,cantidad)

        return array_VA_poisson


    def calcular_frecuencias_por_intervalo(self, variables_aleatorias, cantidad_intervalos):
         # Convierto tipos de datos
         # Convierto tipos de datos
        cantidad_intervalos = int(cantidad_intervalos)

        # Inicializo datos
        minimo = min(variables_aleatorias)
        maximo = max(variables_aleatorias)
        paso = round(((maximo - minimo) / cantidad_intervalos), 2)
        intervalos = []
        frecuencias_x_intervalo = {}

        # Genero lista de intervalos e inicializo keys en diccionario de frecuencias por intervalo
        for i in range(0, cantidad_intervalos):
            min_intervalo = round(minimo, 2)
            if min_intervalo == int(min_intervalo):
                min_intervalo = int(min_intervalo)
            max_intervalo = round(min_intervalo + paso, 2)
            if max_intervalo == int(max_intervalo):
                max_intervalo = int(max_intervalo)
            media_intervalo = round(((min_intervalo + max_intervalo) / 2), 2)
            if media_intervalo == int(media_intervalo):
                media_intervalo = int(media_intervalo)
            intervalos.append({
                "minimo": min_intervalo,
                "maximo": max_intervalo,
                "media": media_intervalo
            })
            frecuencias_x_intervalo[media_intervalo] = 0
            minimo = max_intervalo

        # Genero diccionario de frecuencias por intervalo
        for variable_aleatoria in variables_aleatorias:
            for intervalo in intervalos:
                if intervalo.get("minimo") <= variable_aleatoria < intervalo.get("maximo"):
                    frecuencias_x_intervalo[intervalo["media"]] += 1

        # Genero listas de medias y frecuencias observadas a partir de datos anteriores
        medias = [str(intervalo.get("media")).replace(".", ",") for intervalo in intervalos]
        frecuencias_obsevadas = list(frecuencias_x_intervalo.values())

        # Inicializo lista de frecuencias esperadas
        frecuencias_esperadas = []
        

        # Genero lista de frecuencias esperada a partir de datos anteriores para distribucion normal
        elif tipo_distribucion == 0:
            media = statistics.mean(variables_aleatorias)
            desviacion_estandar = statistics.stdev(variables_aleatorias)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.norm(media, desviacion_estandar).cdf(intervalo.get("maximo")) -
                                             stats.norm(media, desviacion_estandar).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        # Genero lista de frecuencias esperada a partir de datos anteriores para distribucion exponencial negativa
        elif tipo_distribucion == 1:
            media = statistics.mean(variables_aleatorias)
            for intervalo in intervalos:
                frecuencia_esperada = round((stats.expon(media).cdf(intervalo.get("maximo")) -
                                             stats.expon(media).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        # Genero lista de frecuencias esperada a partir de datos anteriores para distribucion poisson
        elif tipo_distribucion == 2:
            media = statistics.mean(variables_aleatorias)
                for intervalo in intervalos:
                    frecuencia_esperada = round((stats.poisson(media).cdf(intervalo.get("maximo")) -
                                             stats.poisson(media).cdf(intervalo.get("minimo"))) *
                                            len(variables_aleatorias), 2)
                frecuencias_esperadas.append(frecuencia_esperada)

        return medias, frecuencias_obsevadas, frecuencias_esperadas


    


    def generar_grafico_frecuencias(self, medias, frecuencias_observadas, frecuencias_esperadas):

        # Creo grafico
        x = numpy.arange(len(medias))
        width = 0.35
        fig, ax = pyplot.subplots()
        rects1 = ax.bar(x - width / 2, frecuencias_observadas, width, label="Observadas")
        rects2 = ax.bar(x + width / 2, frecuencias_esperadas, width, label="Esperadas")

        ax.set_ylabel("Cantidad")
        ax.set_title("Frecuencias esperadas y observadas")
        ax.set_xticks(x)
        ax.set_xticklabels(medias)
        ax.legend()

        for rect in rects1:
            height = rect.get_height()
            ax.annotate("{}".format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                        textcoords="offset points", ha="center", va="bottom")
        for rect in rects2:
            height = rect.get_height()
            ax.annotate("{}".format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                        textcoords="offset points", ha="center", va="bottom")
        fig.tight_layout()
        pyplot.show()

    def prueba_Chi_Cuadrado(self,frecuencias_observadas,frecuencias_esperadas):
         # Inicializo datos
        cantidad_intervalos = len(frecuencias_observadas)
        chi_cuadrado = 0

        # Calculo valor chi cuadrado
        for i in range(cantidad_intervalos):
            valor_intervalo = ((frecuencias_observadas[i] - frecuencias_esperadas[i]) ** 2) / frecuencias_esperadas[i] \
                if frecuencias_esperadas[i] != 0 else 0
            chi_cuadrado += valor_intervalo

        chi_cuadrado = round(chi_cuadrado, 2)
        if chi_cuadrado == int(chi_cuadrado):
            chi_cuadrado = int(chi_cuadrado)

        return chi_cuadrado

