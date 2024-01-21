import math
import os
import cv2
import random
# from random import *
from Individuo import *
import matplotlib.pyplot as plt
import sympy as sp


class AGS:
    num_generacion = 0
    pob_cruza = []
    pob_muta = []
    poblacion_init = []
    poblacion_max = []
    poblacion_min = []
    poblacion_final = []
    poblacion_generacion = []

    def __init__(self, pc, pmi, pmg, po, p_Max, rango_min, rango_max, interv, cantidad_gene, formula):
        self.pc = pc
        self.pmi = pmi
        self.pmg = pmg
        self.po = po
        self.p_Max = p_Max
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.interv = interv
        self.cantidad_gene = cantidad_gene
        self.formula = formula

        rango = rango_max - rango_min
        # Calcular exponente, es decir tamaño de alelo
        puntos = (rango / interv) + 1
        exponente = 1
        while True:
            exponente += 1
            bits = 2 ** exponente
            if bits >= puntos:
                break

        self.poblacion_generacion.clear()
        while True:
            self.pob_cruza.clear()
            self.pob_muta.clear()
            self.poblacion_init.clear()
            self.poblacion_max.clear()
            self.poblacion_min.clear()
            self.poblacion_final.clear()

            self.fun_poblacion_init(exponente, rango, interv, po, formula)
            self.cruza(pc, po, exponente, rango, interv, formula)
            self.mutacion(pmi, pmg, rango, interv)
            self.poda(p_Max, rango_max, rango_min)
            self.num_generacion += 1
            if self.num_generacion == self.cantidad_gene:
                break

        self.grafico_print()


    def fun_poblacion_init(self, exponente, rango, interv, po, formula):
        for i in range(po):
            alelo_c = ""
            for o in range(exponente):
                alelo_c = alelo_c + str(random.choice(["0", "1", "0", "1", "0"]))

            self.poblacion_init.append(self.creacion_indiv(alelo_c, rango, interv, formula))

    def creacion_indiv(self, alelo_c, rango, interv, formula):
        valor_c = 0
        for posicion, digito_string in enumerate(alelo_c[::-1]):
            valor_c += int(digito_string) * 2 ** posicion

        fenotipo = self.fenotipo(rango, interv, valor_c)
        aptitud = self.aptitud(fenotipo, formula)
        individuo = Individuo(alelo_c, valor_c, fenotipo, aptitud)

        return individuo

    def cruza(self, pc, po, exponente, rango, interv, formula):
        # tam_pob_cruce = len(self.poblacion_init)
        num_parejas = int(pc * po / 2)

        for _ in range(num_parejas):
            pareja = random.sample(range(po), 2)

            if random.random() <= pc:
                punto_cruce = random.randint(1, exponente - 1)
                alelo_1 = self.poblacion_init[pareja[0]].alelo[:punto_cruce] + self.poblacion_init[pareja[1]].alelo[
                                                                               punto_cruce:]
                alelo_2 = self.poblacion_init[pareja[1]].alelo[:punto_cruce] + self.poblacion_init[pareja[0]].alelo[
                                                                               punto_cruce:]

                hijo_1 = self.creacion_indiv(alelo_1, rango, interv, formula)
                hijo_2 = self.creacion_indiv(alelo_2, rango, interv, formula)

                self.pob_cruza.extend([hijo_1, hijo_2])

    def aptitud(self, fenotipo, formula):
        # Crear el símbolo x
        x = sp.symbols('x')

        # Convertir la fórmula de la cadena a una expresión simbólica
        expr = sp.sympify(formula)

        # Sustituir x por el fenotipo en la expresión
        expr_sustituida = expr.subs(x, fenotipo)

        # Evaluar la expresión sustituida
        aptitud = sp.N(expr_sustituida)

        return aptitud


    # Poda Estrategia P2 limitando rango con respecto al fenotipo
    def poda(self, num_pobmax, rango_max, rango_min):
        poblacion_en_rango = [indv for indv in self.poblacion_init if rango_min <= indv.fenotipo <= rango_max]

        if not poblacion_en_rango:
            print("¡Advertencia! La población en rango está vacía.")
            return []

        # Ordenar población en rango por aptitud en orden descendente
        poblacion_ordenada = sorted(poblacion_en_rango, key=lambda x: x.aptitud, reverse=True)

        if not poblacion_ordenada:
            print("¡Advertencia! La población ordenada está vacía.")
            return []

        # ESTRATEGIA P2: Conservar el mejor individuo y eliminar el resto aleatoriamente
        self.poblacion_final = [poblacion_ordenada[0]] + random.sample(poblacion_ordenada[1:],
                                                                       min(num_pobmax - 1, len(poblacion_ordenada) - 1))

        print("-----------POBLACION FINAL MAXIMA-------------")
        if self.num_generacion >= len(self.poblacion_generacion):
            self.poblacion_generacion.append([])

        for i, indv in enumerate(self.poblacion_final):
            print(
                f"ID: {i + 1}, Alelo: {indv.alelo}, Valor: {indv.valor}, Fenotipo: {indv.fenotipo}, Aptitud: {indv.aptitud}, Generacion: {self.num_generacion}")
            self.poblacion_generacion[self.num_generacion].append(indv.aptitud)

    def mutacion(self, pmi, pmg, rango, interv):
        for indv in self.poblacion_final:
            if random.random() <= pmi:
                alelo_mutado = ""
                for bit in indv.alelo:
                    if random.random() <= pmg:
                        alelo_mutado += '1' if bit == '0' else '0'
                    else:
                        alelo_mutado += bit

                nuevo_indv = self.creacion_indiv(alelo_mutado, rango, interv)
                self.pob_muta.append(nuevo_indv)

    def fenotipo(self, rango, interv, indv_valor):
        fenotipo = ((rango / 2) + indv_valor) * interv
        return fenotipo

    def test_print(self):
        print("------------POB INICIAL--------------")
        for indv in self.poblacion_init:
            print(f"Alelo: {indv.alelo}, Valor: {indv.valor}, Fenotipo: {indv.fenotipo}, Aptitud: {indv.aptitud}")

        print("----------POB--CRUZA----------------")
        for indv in self.pob_cruza:
            print(f"Alelo: {indv.alelo}, Valor: {indv.valor}, Fenotipo: {indv.fenotipo}, Aptitud: {indv.aptitud}")

        print("----------POB--MUTA----------------")
        for indv in self.pob_muta:
            print(f"Alelo: {indv.alelo}, Valor: {indv.valor}, Fenotipo: {indv.fenotipo}, Aptitud: {indv.aptitud}")

        print("Columna:", self.poblacion_generacion)

    def grafico_print(self):
        list_max = []
        list_min = []
        list_promedio = []

        mejores_individuos = []
        peores_individuos = []
        promedio_individuos = []

        for i in range(len(self.poblacion_generacion)):
            # Obtener el mejor individuo de la generación
            mejor_individuo = max(self.poblacion_final, key=lambda x: x.aptitud)
            mejores_individuos.append(mejor_individuo)

            # Obtener el peor individuo de la generación
            peor_individuo = min(self.poblacion_final, key=lambda x: x.aptitud)
            peores_individuos.append(peor_individuo)

            # Calcular el promedio de aptitud
            promedio = sum(self.poblacion_generacion[i]) / len(self.poblacion_generacion[i])
            promedio_individuos.append(promedio)

            list_max.append(mejor_individuo.aptitud)
            list_min.append(peor_individuo.aptitud)
            list_promedio.append(promedio)

        # Crear gráfico
        generaciones = list(range(len(self.poblacion_generacion)))

        # Gráfico del mejor individuo
        plt.plot(generaciones, [indv.aptitud for indv in mejores_individuos], label='Mejor Individuo', marker='o')

        # Gráfico del peor individuo
        plt.plot(generaciones, [indv.aptitud for indv in peores_individuos], label='Peor Individuo', marker='o')

        # Gráfico del promedio de individuos
        plt.plot(generaciones, list_promedio, label='Promedio de Individuos', marker='o')

        plt.xlabel('Número de Generación')
        plt.ylabel('Aptitud')
        plt.legend()
        plt.title('Evolución de la Aptitud a lo largo de las Generaciones')
        plt.switch_backend('TkAgg')
        plt.show()

    def graphi_generation(self):
        # Crear la carpeta 'images' si no existe
        if not os.path.exists('images'):
            os.makedirs('images')

        fenotipos = [indv.fenotipo for indv in self.poblacion_final]

        for i, generacion in enumerate(self.poblacion_generacion):
            # Obtener el mejor individuo de la generación
            mejor_individuo = max(self.poblacion_final, key=lambda x: x.aptitud)

            # Crear gráfico de dispersión
            plt.scatter(mejor_individuo.fenotipo, mejor_individuo.aptitud, color='blue', marker='o')
            plt.xlabel('Fenotipo')
            plt.ylabel('Aptitud')
            plt.title(f'Dispersión del Mejor Individuo - Generación {i + 1}')

            # Guardar la imagen en la carpeta 'images'
            plt.savefig(f'images/generacion_{i + 1}.png')
            plt.close()  # Cerrar el gráfico actual para evitar superposiciones

        path = './images/'
        archivos = sorted(os.listdir(path))
        img_array = []

        for x in range (0,len(archivos)):
            nomArchivo = archivos[x]
            dirArchivo = path + str(nomArchivo)
            img = cv2.imread(dirArchivo)
            img_array.append(img) 
        height, width  = img.shape[:2]
        video = cv2.VideoWriter('generaciones.avi', cv2.VideoWriter_fourcc(*'DIVX'), 2, (width,height))

        #Colocar los frames en video
        for i in range(0, len(archivos)):
            video.write(img_array[i])
            
        #liberar
        video.release()
        

        # Crear gráfico de dispersión general
        plt.scatter(fenotipos, [indv.aptitud for indv in self.poblacion_final], color='blue', marker='o')
        plt.xlabel('Fenotipo')
        plt.ylabel('Aptitud')
        plt.title('Dispersión del Mejor Individuo en Cada Generación')
        plt.show()

        print("Gráficas de dispersión generadas y guardadas en la carpeta 'images'.")
