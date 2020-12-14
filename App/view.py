"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
from time import process_time
import timeit
assert config



from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de Taxis")
    print("3- Requerimiento 1")
    print("4- Requerimiento 2a")
    print("5- Requerimiento 2b")
    print("6- Requerimiento 3")
    print("0- Salir")
    print("*******************************************")


while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de Rutas Taxis ....")
        t1 = process_time()

        controller.loadFile(cont) 

        print("Muestar carga")
        t2 = process_time()
        t = t2-t1
        print("Tiempo requerido: ", t)


  
    elif int(inputs[0]) == 3:
        m = int(input("Top M compañias por texis Afiliados: "))
        n = int(input("Top N compañias por Servicios Realizados: "))

        print("Numero Total de Taxis : ", cont['totalTaxi'])
        print("Numero Total de compañias : ", lt.size(cont['lstTaxi']))

        #ordenar por Numero de taxis
        controller.ordenar(cont,1)
        print("")
        print(m, " Compañias con mas taxis afiliados:\n")

        itera = it.newIterator(cont['lstTaxi'])
        i=1
        while it.hasNext(itera):
            elemento = it.next(itera)
            print("Nombre de la Compañia  : ",elemento['company_name'])
            print("Numero Taxis Afiliados: ", elemento['n_taxis'])
            print("")
            if (i >= m):
                break
            i = i+1

        
        #Ordenar por Numero de servicios
        controller.ordenar(cont,2)
        print("")
        print(n, " Compañias con mas Servicios realiados:\n")

        itera = it.newIterator(cont['lstTaxi'])
        i=1
        while it.hasNext(itera):
            elemento = it.next(itera)
            print("Nombre de la Compañia  : ",elemento['company_name'])
            print("Numero de Servicios : ",elemento['n_servicios'])
            print("")
            if (i >= n):
                break
            i = i+1


    elif int(inputs[0]) == 4:
        print('N taxis con mas puntos en una fecha ')
        
        f = input("Indique Fecha  (YYYY-MM-DD): ")
        n = int(input("Numero de Taxis "))
        lst = controller.puntosPorFecha(cont, f,n)
        for ele in lst:
            print("taxi id : ", ele['Taxi'])
            print("Puntos : ", round(ele['puntos'],2))
            print("")

       
    
    elif int(inputs[0]) == 5:
        print('M taxis con mas puntos en un rango de fechas ')
        
        f1 = input("Indique Fecha inicial  (YYYY-MM-DD): ")
        f2 = input("Indique Fecha final    (YYYY-MM-DD): ")
        n = int(input("Numero de Taxis "))

        lst = controller.puntosPorRangoFecha(cont, f1,f2, n)
        for ele in lst:
            print("taxi id : ", ele['Taxi'])
            print("Puntos : ", ele['puntos'])
            print("")

        
       
    
    elif int(inputs[0]) == 6:
        
        stacion_ini = "28"


        # Rutas de costo minimo de estacion inicial a demas estaciones

        paths = controller.minimumCostPaths(cont, stacion_ini) 

        stacion_fin = "56"
        #Ruta de costo minimo entre estacion inicial y estacion final
        path = controller.minimumCostPath(paths, stacion_fin)

        ruta =[]

        if path is not None:
            pathlen = stack.size(path) #Porque viene en forma de pila
            print('El camino es de longitud: ' + str(pathlen))
            while (not stack.isEmpty(path)):
                stop = stack.pop(path)
                print(stop)
                ruta.append(stop['vertexA'] + "-" + stop['vertexB'])
        else:
            print('No hay camino')

        hora_ini = int('80')
        hora_fin = int('1230')

        lst = controller.rutasPorRangoHora(cont, hora_ini,hora_fin,ruta)

        print("mejor Horario :")

        print(lst)
        

    else:
        sys.exit(0)
sys.exit(0)
