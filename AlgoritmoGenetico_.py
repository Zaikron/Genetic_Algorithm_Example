# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 20:28:44 2022

@author: anthony sandoval

        Articulo    Cal     Peso
    1   Leche       500     0.5
    2   Galleta     300     0.1
    3   Agua        100     0.5
    4   Pan         700     0.25
    5   Huevo       300     0.15
    6   Nueces      400     0.15
    7   Yogurt      500     0.5
    8   Manzana     400     0.3
    
    Poblacion = 4
    Minimo de Calorias = 2000
    Peso Maximo = 2.0Kg

"""
            
import numpy as np
from numpy import random
import math
import matplotlib.pyplot as plt

individuos = 4 #Numero de individuos en la poblacion
cromosoma = 8 #Numero de genes en un cromosoma
minCal = 2000.0 #Minimo de calorias de los alimentos llevados
maxPeso = 2.0 #Maximo peso de la mochina en kg

generaciones = 50 #Numero de veces que se repetira el algoritmo
#Calorias y pesos de los articulos
articulos = [
                [500, 0.5],
                [300, 0.1],
                [100, 0.5],
                [700, 0.25],
                [300, 0.15],
                [400, 0.15],
                [500, 0.5],
                [400, 0.3],
            ]
nombreArticulos = ['Leche', 'Galleta', 'Agua', 'Pan', 'Huevo', 'Nueces', 'Yogurt', 'Manzana']
calCol = 0 #Numero de columna de las calorias para ubicarlas en la matriz de acticulos
pesoCol = 1 #Numero de columna del peso para ubicarlo en la matriz de acticulos
calTotal = 0.0 #Numero total de calorias, global, de cada generacion
pesoTotal = 0.0 #Numero total de peso, global, de cada generacion
#Variable para guardar el indice del peor individuo, cambiado a los valores del mejor, para ignorarlo a la hora de mutar
individuoMenorCambiado = 0 

fitPorcentajes = 5 #Numero de columnas para la matriz en la que se guardan los valores fitness
fitnessValues = np.zeros((individuos, fitPorcentajes)) #Matriz para guardar los valores fitness de la poblacion
fitPeso = 0 #Numero de la columna para la suma del peso del individuo 
fitCal = 1 #Numero de la columna para la suma de calorias del individuo 
fitPesoPorcent = 2 #Numero de la columna para el porcentaje de calorias del individuo 
fitCalPorcent = 3 #Numero de la columna para el porcentaje de peso del individuo 
fitTotal = 4 ##Numero de la columna para la suma de porcentajes de peso y calorias del individuo

    ########## IMPRESION DE LOS DATOS ##########
def imprimirPoblacion(poblacion):
    for individuo in range(individuos):
        for gen in range(cromosoma):
            print(poblacion[individuo][gen], end = " ")
        print()
    print('-------------------------------------------------------')

def imprimirFitness(fitnessValues):
    for individuo in range(individuos):
        for valor in range(fitPorcentajes):
            print("{:.2f}".format(fitnessValues[individuo][valor]), end = " ")
        print()
    print('-------------------------------------------------------')
    
    ########## Metodo para encontrar al individuo mas fuerte ##########
def masFuerte():
    fuerte = 0
    indiceFuerte = 0
    for individuo in range(individuos):
        if(fitnessValues[individuo][fitTotal] > fuerte):
            fuerte = fitnessValues[individuo][fitTotal]
            indiceFuerte = individuo
    return indiceFuerte

    ########## Metodo para encontrar al individuo mas debil ##########
def masDebil():
    debil = math.inf
    indiceDebil = 0
    for individuo in range(individuos):
        if(fitnessValues[individuo][fitTotal] < debil):
            debil = fitnessValues[individuo][fitTotal]
            indiceDebil = individuo
    return indiceDebil

    ########## Metodo para mutar individuos ##########
def mutacion():
    #En la mutacion solo se cambia un bit aleatorio de cada individuo, se tiene que ingnorar a algun individuo
    #En mi caso el individuo ignorado es el mas debil que fue cambiado por el fuerte
    for individuo in range(individuos):
        if(individuo != individuoMenorCambiado):
            mutado = random.randint(0, cromosoma)
            if(poblacion[individuo][mutado] == 1):
                poblacion[individuo][mutado] = 0
            elif(poblacion[individuo][mutado] == 0):
                poblacion[individuo][mutado] = 1

    ########## Metodo para intercambiar genes entre dos individuos, necesario para el metodo cruzamiento() ##########
def intercambio(individuo1, individuo2, punto):
    aux1 = -1
    aux2 = -1
    #Aqui se hace un intercambio de valores entre individuos a partir del indice indicado por la variable punto
    for gen in range(punto, cromosoma):
        aux1 = poblacion[individuo1][gen]
        aux2 = poblacion[individuo2][gen]
        poblacion[individuo1][gen] = aux2
        poblacion[individuo2][gen] = aux1
    
    ########## Metodo para cruzar dos individuos ##########
def cruzamiento():
    puntoCruz = random.randint(2, cromosoma-2)
    
    for individuo in range(individuos):
        if(individuo % 2 == 0): #Esta condicion es para que ingnore al segundo individuo
            intercambio(individuo, individuo+1, puntoCruz)
            
    ########## Metodo para calcular los porcentajes de peso, calorias y total ##########
def calcularPorcentajeFitness():
    for individuo in range(individuos):
        # calorias / calorias totales * 100
        # peso / peso total * 100
        porcentCal = (fitnessValues[individuo][fitCal] /calTotal) * 100
        porcentPeso = (fitnessValues[individuo][fitPeso] /pesoTotal) * 100
        
        fitnessValues[individuo][fitCalPorcent] = porcentCal
        fitnessValues[individuo][fitPesoPorcent] = porcentPeso
        fitnessValues[individuo][fitTotal]  = porcentCal + porcentPeso

    ########## Metodo para obtener las calorias totales de un individuo ##########
def indCalorias(individuo):
    calorias = 0
    for gen in range(cromosoma):
        if(individuo[gen] == 1):
            calorias += articulos[gen][calCol]
    return calorias

    ########## Metodo para obtener el peso total de un individuo ##########
def indPeso(individuo):
    peso = 0
    for gen in range(cromosoma):
        if(individuo[gen] == 1):
            peso += articulos[gen][pesoCol]
    return peso

    ########## Metodo para calcular el fitness de la poblacion ##########
def fitness():
    global calTotal
    global pesoTotal
    calTotal = 0
    pesoTotal = 0
    
    for individuo in range(individuos):
        #Se obtienen calorias y peso total de cada individuo
        calorias = indCalorias(poblacion[individuo])
        peso = indPeso(poblacion[individuo])
        #En fitnessValues se van guardando los valores obtenidos respecto a los indices de los individuos
        fitnessValues[individuo][fitCal] = calorias
        fitnessValues[individuo][fitPeso] = peso
        #Aqui se hace la sumatoria de las calorias y peso de la generacion
        calTotal += calorias
        pesoTotal += peso
    calcularPorcentajeFitness()

    ########## Metodo para crear un individuo ##########
def crearIndividuo():
    ind = np.random.randint(2, size=(cromosoma), dtype=('int32'))
    #Se hace una comprobacion para que el peso no pase del maximo y las calorias no pasen del minimo
    while((indCalorias(ind) < minCal) or (indPeso(ind) > maxPeso)): 
        ind = crearIndividuo() #Se crearan nuevos individuos hasta que los valores esten dentro del rango
    return ind

    ########## Metodo para crear una poblacion, requiere del metodo crearIndividuo() ##########      
def crearPoblacion():
    poblacion = np.zeros((individuos, cromosoma), dtype=('int32'))
    for individuo in range(individuos):
        poblacion[individuo] = crearIndividuo()
    return poblacion

    ########## Metodo para actualizar la poblacion y crear una nueva generacion ##########
def nuevaGeneracion():
    global poblacion
    global calTotal
    global pesoTotal
    for individuo in range(individuos):
        #Se hace una comprobacion para que el peso no pase del maximo y las calorias no pasen del minimo
        if((indCalorias(poblacion[individuo]) < minCal) or (indPeso(poblacion[individuo]) > maxPeso)):
            poblacion[individuo] = crearIndividuo() #Si hay un individuo incorrecto entonces se crea uno nuevo
    #Recalculo de fitness con la nuegeneracionva 
    fitness()

    ########## Metodo para encontrar al mejor individuo ##########
def masAptoTotal(generacion):
    global mejorIndividuo
    global generacionMejor
    global mejorIndCromosoma
    for individuo in range(individuos):
        if(fitnessValues[individuo][fitTotal] > mejorIndividuo[fitTotal]):
            for gen in range(cromosoma):
                mejorIndCromosoma[gen] = poblacion[individuo][gen]
            for valor in range(fitPorcentajes):
                mejorIndividuo[valor] = fitnessValues[individuo][valor]
                generacionMejor = generacion
                

#Creacion de la poblacion
poblacion = crearPoblacion()
#Variables para visualizar el mejor individuo
mejorIndividuo = np.zeros((fitPorcentajes), dtype=('float32'))
mejorIndCromosoma = np.zeros((cromosoma), dtype=('int32'))
generacionMejor = 0
#Variables para graficar
x = np.zeros((generaciones+1), dtype=('float32'))
y = np.zeros((generaciones+1), dtype=('float32'))

#Se calcula el fitness por primera vez
fitness()
print('POBLACION INICIAL')
imprimirPoblacion(poblacion)
imprimirFitness(fitnessValues)

for i in range(generaciones+1): #Se repite el algoritmo la veces que se indique en generaciones
    print('________GENERACION ', i, '________')

    #Seleccion
    individuoMenorCambiado = masDebil() #Se guarda el individuo mas debil de la poblacion
    poblacion[masDebil()] = poblacion[masFuerte()] #Se intercambia el individuo mas debil con el mas fuerte de la poblacion
    print('SELECCION: ELIMINACION DEL INDIVIDUO MAS DEBIL')
    imprimirPoblacion(poblacion)
    #Cruzamiento entre individuos de la poblacion
    cruzamiento()
    print('CRUZAMIENTO')
    imprimirPoblacion(poblacion)
    #Mutacion
    mutacion()
    print('MUTACION')
    imprimirPoblacion(poblacion)
    #Se calcula de nuevo fitness para los individuos modificados
    fitness()
    print('CALCULO DEL FITNESS CON INDIVIDUOS MODIFICADOS')
    imprimirFitness(fitnessValues)
    #Se crea una nueva generacion, los que no cumplen se eliminan y entran nuevos individuos
    #Se recalcula el fitness de la nueva generacion dentro de la funcion
    nuevaGeneracion()
    print('SE CREA LA NUEVA GENERACION')
    imprimirPoblacion(poblacion)
    imprimirFitness(fitnessValues)
    
    masAptoTotal(i)
    imprimirFitness(fitnessValues)
    
    y[i] = mejorIndividuo[fitTotal]
    x[i] = i


print('MEJOR INDIVIDUO')
np.set_printoptions(suppress=True)
print(mejorIndividuo)
print('En la generacion: ', generacionMejor)
print()
print('ARTICULOS: ')
for gen in range(cromosoma):
    if(mejorIndCromosoma[gen] == 1):
        print(nombreArticulos[gen], ', ', end = ' ')
        

#Grafica de las generaciones y mejores individuos
plt.plot(x, y, color='red', linewidth=3)
plt.show()
