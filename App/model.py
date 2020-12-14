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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me

from DISClib.Algorithms.Sorting import  mergesort as merSort

import datetime

assert config


"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo


def newAnalyzer():

    analyzer = {'graphTaxi': None, 
                'mapaTaxi': None , 
                'lstTaxi': None , 
                'totalTaxi': None }

    analyzer["graph"] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=1000,
                                    comparefunction=compareStations)

    analyzer['hora'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHora)

    
    analyzer['mapaTaxi'] =  om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)

    analyzer['lstTaxi'] = lt.newList('SINGLE_LINKED', comparar_company)

    analyzer['totalTaxi'] =0

    return analyzer


# ==============================
# Funciones de consulta
# ==============================
def es_numero(s):
    try:
        s =float(s)
        return s
    except ValueError:
        return 0

# ==============================
# Funciones Helper
# ==============================

def addTrip(analyzer,trip):
    actualizaLista(analyzer,trip)
    actualizaMapa(analyzer,trip)
    actualizaGrafo(analyzer,trip)
    actualizaHora(analyzer,trip)
    return analyzer

def actualizaHora(analyzer,trip):
    mapaHora = analyzer['hora']
    fechaa = trip['trip_start_timestamp']
    hora = aproxima_hora(fechaa)
    entry = om.get(mapaHora,hora)
    if entry is None:
        valormapaHora = {'lstRutas':None }
        valormapaHora['lstRutas'] = lt.newList('SINGLE_LINKED', compararRuta)
        om.put(mapaHora,hora,valormapaHora)
        
    else:
        valormapaHora = me.getValue(entry)
    actualizaMapaHora(valormapaHora,trip)
    
    return mapaHora

def actualizaMapaHora(valormapaHora,trip):

    origen = es_numero(trip["pickup_community_area"])
    origen = str(int(origen))

    destino = es_numero(trip["dropoff_community_area"])
    destino = str(int(destino))

    duracion = es_numero(trip['trip_seconds'])
    duracion = int(duracion)

    ruta = origen + "-" + destino

    pos = lt.isPresent(valormapaHora['lstRutas'],ruta)
    if pos == 0:
        valor = {'idRuta': None, 'lstTiempo': None, 'promedio': None}
        valor['idRuta'] = ruta
        valor['lstTiempo'] = lt.newList()
        lt.addLast(valor['lstTiempo'], duracion)

        lt.addLast(valormapaHora['lstRutas'],valor)
    else:
        valor = lt.getElement(valormapaHora['lstRutas'],pos)
        lt.addLast(valor['lstTiempo'], duracion)
    
    return valormapaHora



def compararRuta(ele1,ele2):
    ele2 = ele2['idRuta']
    if ele1 == ele2:
        return 0
    return 1



def actulizarRuta(analyzer):

    lstValores = om.valueSet(analyzer['hora'])
    itera = it.newIterator(lstValores)

    while(it.hasNext(itera)):
        valor = it.next(itera) 
        lstValor = valor['lstRutas']
        
        itera2 = it.newIterator(lstValor)
        while(it.hasNext(itera2)):
            val = it.next(itera2)  #{'idRuta': None, 'lstTiempo': None, 'promedio': None}

            #obtener promedio de lstTiempo
            promedio =0
            itera3 = it.newIterator(val['lstTiempo'])
            while(it.hasNext(itera3)):
                tiempo = it.next(itera3)
                promedio = promedio + tiempo

            val['promedio'] = promedio / lt.size(val['lstTiempo'])
    return analyzer



def actualizaGrafo(analyzer,trip):
    origen = es_numero(trip["pickup_community_area"])
    origen = str(int(origen))

    destino = es_numero(trip["dropoff_community_area"])
    destino = str(int(destino))

    duracion = es_numero(trip["trip_miles"])
    duracion = int(duracion)

    addStation(analyzer, origen)
    addStation(analyzer, destino)
    addConnection(analyzer, origen, destino, duracion)

def addStation(analyzer, id):

    if not gr.containsVertex(analyzer["graph"], id):
        gr.insertVertex(analyzer["graph"], id)
    return analyzer


def addConnection(analyzer, origen, destino, duracion):

    arco = gr.getEdge(analyzer["graph"], origen, destino)
    if arco is None:
        gr.addEdge(analyzer["graph"], origen, destino, duracion)
    
    return analyzer



def actualizaMapa(analyzer,trip):

    fecha = trip['trip_start_timestamp']
    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%f')
    fecha = fecha.date()
    entry = om.get(analyzer['mapaTaxi'],fecha)

    if entry is None:
        entrada = {'lstidtaxi':None }
        entrada['lstidtaxi'] = lt.newList('SINGLE_LINKED', compararTaxi)
        om.put(analyzer['mapaTaxi'],fecha,entrada)
    else:
        entrada = me.getValue(entry)
    
    actualizataxi(entrada,trip)

    return analyzer

'''
def actualizaMapa1(analyzer,trip):

    fecha = trip['trip_start_timestamp']
    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%f')
    fecha = fecha.date()
    entry = om.get(analyzer['mapaTaxi'],fecha)

    if entry is None:

        entrada = {'mapaidtaxi':None }
        entrada['mapaidtaxi'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compararId)

        om.put(analyzer['mapaTaxi'],fecha,entrada)

    else:
        entrada = me.getValue(entry)
    
    actualizataxi1(entrada,trip)

    return analyzer
'''        

def actualizataxi(entrada,trip):

    millas = es_numero(trip['trip_miles'])
    total = es_numero(trip['trip_total'])
    tax_id = trip['taxi_id'].strip()
    pos = lt.isPresent(entrada['lstidtaxi'],tax_id)

    if pos ==0:
        value =  {'idtaxi': None, 'servicios':None, 'millas':None, 'totalDinero': None, 'puntos': None}

        value['idtaxi'] = tax_id
        value['millas'] = millas
        value['totalDinero'] = total
        value['servicios'] = 1
        lt.addLast(entrada['lstidtaxi'],value)
    else:
        value = lt.getElement(entrada['lstidtaxi'],pos)
        value['servicios'] += 1
        value['millas'] += millas
        value['totalDinero'] += total

    return entrada

'''
def actualizataxi1(entrada,trip):

    millas = es_numero(trip['trip_miles'])
    total = es_numero(trip['trip_total'])
    entry = m.get(entrada['mapaidtaxi'],trip['taxi_id'])

    if entry is None:
 
        value ={'servicios':None, 'millas':None, 'totalDinero': None, 'puntos': None}       
 
        value['millas'] = millas
        value['totalDinero'] = total
        value['servicios'] = 1

        m.put(entrada['mapaidtaxi'],trip['taxi_id'],value)
    else:
        value = me.getValue(entry)
        value['servicios'] = value['servicios'] + 1
        value['millas'] = value['millas'] + millas
        value['totalDinero'] = value['totalDinero'] + total
    
    return entrada
'''
def nuevaEntrada(trip):

    entrada = {'mapaidtaxi':None }
    
    entrada['mapaidtaxi'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compararId)
    
    return entrada


def actualizaLista(analyzer,trip):
    compania = trip['company'].strip()
    if compania == "" :
        compania = "Independent Owner"

    pos = lt.isPresent(analyzer['lstTaxi'],compania)      
    total_taxi =0     
    if pos ==0:
        elemento ={'company_name': None, 'lst_taxi_id':None , 'n_taxis': None , 'n_servicios':None}

        elemento['company_name'] = compania
        elemento['lst_taxi_id'] = lt.newList('SINGLE_LINKED', compararIdTaxi)
        lt.addLast(elemento['lst_taxi_id'],trip['taxi_id'])
        elemento['n_taxis'] =1
        elemento['n_servicios']=1
        lt.addLast(analyzer['lstTaxi'],elemento)

        total_taxi = 1

    else:
        elemento = lt.getElement(analyzer['lstTaxi'], pos)
        elemento['n_servicios'] = elemento['n_servicios'] +1
        pos1 = lt.isPresent(elemento['lst_taxi_id'],trip['taxi_id'])
        if pos1 ==0:
            lt.addLast(elemento['lst_taxi_id'],trip['taxi_id'])
            elemento['n_taxis'] = elemento['n_taxis'] +1
            total_taxi = 1

    analyzer['totalTaxi'] += total_taxi
    
    return analyzer
    

# ==============================
# Funciones de Comparacion
# ==============================

def funcioncomparacion_Ntaxi(elem1, elem2):
    if elem1['n_taxis']  > elem2['n_taxis']:
        return True
    return False


def funcioncomparacion_Nserv(elem1, elem2):
    
    if elem1['n_servicios']  > elem2['n_servicios']:
        return True
    return False


def funcioncomparacion(elem1, elem2):
    if elem1['n_taxis']  > elem2['n_taxis']:
        return True
    return False

def comparar_company(c1,c2):
    if c1 == c2['company_name']:
        return 0
    return 1

def compararTaxi(taxi1,taxi2):
    taxi2 = taxi2['idtaxi'].strip()
    taxi1 = taxi1.strip()
   
    if taxi1 == taxi2:
        return 0
    return 1

def compararIdTaxi(taxi1, taxi2):
    if taxi1 == taxi2:
        return 0
    return 1

def compararId(taxi1, taxi2):
    taxi2 = me.getKey(taxi2)
    if taxi1 == taxi2:
        return 0
    return 1


def compareDates(date1, date2):
    
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareStations(id1, keyid2):
    """
    Compara dos estaciones
    """
    id2 = keyid2['key']
    if (id1 == id2):
        return 0
    elif (id1 > id2):
        return 1
    else:
        return -1



def ordenar(analyzer, valcampo):
    if valcampo == 1:
        merSort.mergesort(analyzer['lstTaxi'],funcioncomparacion_Ntaxi )
    else:
        merSort.mergesort(analyzer['lstTaxi'],funcioncomparacion_Nserv )
    return analyzer



def muestradatos(analyzer):
    
    keys = om.keySet(analyzer['mapaTaxi'])

    itera = it.newIterator(keys)
    #mapa ordenado
    while(it.hasNext(itera)):
        key = it.next(itera)
        
        entryMapa = om.get(analyzer['mapaTaxi'],key)

        valorMapa = me.getValue(entryMapa)


        itera2 = it.newIterator(valorMapa['lstidtaxi'])
        while(it.hasNext(itera2)):
            valor = it.next(itera2)     #   {'idtaxi': None, 'servicios':None, 'millas':None, 'totalDinero': None, 'puntos': None}
            #if valor['totalDinero'] == 0:
            if('7075c4988c577798c58b800dbb9742376dbbb74a84ce6ead178e7d00afcaafa6ac936cd9af7b6685991b9121b629de30650958fa926c5472da0083a63ed285c7' in valor['idtaxi']  ):

                print(valor['idtaxi'])
                print(valor['servicios'])
                print(valor['millas'])
                print(valor['totalDinero'])
                print(valor['puntos'])
                print("")
                
'''
def muestradatos1(analyzer):
    print("kys mapa por fecha")

    keys = om.keySet(analyzer['mapaTaxi'])
    print(keys)
    
    #print("valores mapa por fecha")
    #print(om.valueSet (analyzer['mapaTaxi']))

    print("valor id taxi")

    itera = it.newIterator(keys)
    while(it.hasNext(itera)):
        key = it.next(itera)
        mapataxi = me.getValue( om.get(analyzer['mapaTaxi'],key))['mapaidtaxi']
        entrada = m.get(mapataxi,'a1b8eb24fa71867de525452474490e1c822269411962feedfe64506a6d777a482fd200afacc5ab57b56a950db16a8e6ddef6c8af1f90642e86c445e4fdce4403')
        if entrada is not None:
            print(me.getValue(entrada))


def actualizaPuntos1(analyzer):
    keys = om.keySet(analyzer['mapaTaxi'])

    itera = it.newIterator(keys)
    #mapa ordenado
    while(it.hasNext(itera)):
        key = it.next(itera)
        
        entryMapa = om.get(analyzer['mapaTaxi'],key)
        valorMapa = me.getValue(entryMapa)
        mapataxi = valorMapa['mapaidtaxi']

        lstValores=  m.valueSet(mapataxi)

        itera2= it.newIterator(lstValores)
        # valores mapa  mapaidtaxi
        while(it.hasNext(itera2)):
            valor = it.next(itera2)  # {'servicios':None, 'millas':None, 'totalDinero': None, 'puntos': None} 
            
            if  valor['totalDinero']  > 0: # hay uno servicios que no tiene valor en trip_total
                 valor['puntos'] = (valor['millas'] / valor['totalDinero']) * valor['servicios']
            else:
                valor['puntos']=0
            
        

    return analyzer     
'''

def actualizaPuntos(analyzer):

    keys = om.keySet(analyzer['mapaTaxi'])
    itera = it.newIterator(keys)

    while(it.hasNext(itera)):
        key = it.next(itera)
        entryMapa = om.get(analyzer['mapaTaxi'],key)
        valorMapa = me.getValue(entryMapa)

        itera2 = it.newIterator(valorMapa['lstidtaxi'])
        while(it.hasNext(itera2)):
            valor = it.next(itera2)

            if  valor['totalDinero']  > 0: # servicios que no tiene valor en trip_total
                 valor['puntos'] = (valor['millas'] / valor['totalDinero']) * valor['servicios']
            else:
                valor['puntos']=0
           

    return analyzer     


def puntosPorFecha(analyzer, fecha,numero):
    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
    entry = om.get(analyzer['mapaTaxi'],fecha)
    valor = me.getValue(entry)
    lsttaxis = valor['lstidtaxi']

    merSort.mergesort(lsttaxis,compararvalores)

    itera = it.newIterator(lsttaxis)
    i =1
    resultado =[]

    while(it.hasNext(itera)):
        valor = it.next(itera)
        salida ={}
        salida['Taxi'] = valor['idtaxi']
        salida ['puntos'] = valor['puntos']
        resultado.append(salida)
        if i >= numero:
            break
        i = i+1



    return resultado

    

def compareHora(h1,h2):
    if (h1 == h2):
        return 0
    elif (h1 > h2):
        return 1
    else:
        return -1


def compararvalores(elem1, elem2):
    if(elem1['puntos']>elem2['puntos']):
        return True
    return False



def puntosPorRangoFecha(analyzer, fecha1,fecha2, numero):
    fecha1 = datetime.datetime.strptime(fecha1, '%Y-%m-%d').date()
    fecha2 = datetime.datetime.strptime(fecha2, '%Y-%m-%d').date()

    lstValores  = om.values(analyzer['mapaTaxi'],fecha1,fecha2)
    
    nueva_lista = lt.newList('SINGLE_LINKED', compararTaxi)

    itera = it.newIterator(lstValores)
    while(it.hasNext(itera)):
        elemto = it.next(itera)
        lista = elemto['lstidtaxi']
        
        itera2 = it.newIterator(lista)
        while(it.hasNext(itera2)):
            valor = it.next(itera2) 
            
            id_taxi =valor['idtaxi']
            puntos = valor["puntos"]
    
            pos = lt.isPresent(nueva_lista, id_taxi)
            if pos ==0:
                salida = {"idtaxi": None, "puntos": None}
                salida["idtaxi"] = id_taxi
                salida["puntos"] = puntos
                lt.addLast(nueva_lista,salida)
            else:
                salida = lt.getElement(nueva_lista,pos)
                salida["puntos"] = salida["puntos"] + puntos
    
    #ordenar lista de salida
    merSort.mergesort(nueva_lista,compararvalores)

    itera = it.newIterator(nueva_lista)
    i =1
    resultado =[]

    while(it.hasNext(itera)):
        valor = it.next(itera)
        salida ={}
        salida['Taxi'] = valor['idtaxi']
        salida ['puntos'] = valor['puntos']
        resultado.append(salida)
        if i >= numero:
            break
        i = i+1
    
    return resultado



def aproxima_hora(fecha):
    hora = fecha[11:13] 
    minutos = fecha[14:16]
 
    minutos = int(minutos)
    hora = int(hora)

    if(minutos == 0):
        minutos =0
    elif(minutos <= 15):
        minutos = "15"
    elif (minutos <= 30):
        minutos ="30"
    elif (minutos<=45):
        minutos ="45"
    elif(minutos <= 59):
        minutos ='0'
        if(hora < 23):
            hora += 1    
        else:
            hora = "0"
    
    hora = str(hora)
    minutos = str(minutos)
 
    hora = int(hora+minutos)

    return hora



def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    paths = djk.Dijkstra(analyzer['graph'], initialStation)
    return paths

def minimumCostPath(paths, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(paths, destStation)
    return path

def rutasPorRangoHora(analyzer, h_ini,h_fin,ruta):

    minimo = 100000000
    cuenta =0
    
    sale ={'horario':None, 'promedio': None}

    lstkeys  = om.keys(analyzer['hora'],h_ini,h_fin)
    itera = it.newIterator(lstkeys)
    while(it.hasNext(itera)):

        key = it.next(itera)
        entry = om.get(analyzer['hora'],key)
        lstvalores = me.getValue(entry)
        itera2 = it.newIterator(lstvalores['lstRutas'])  #lista de rutas
        print("")
        print("inici lista intrena key ",key)

        while(it.hasNext(itera2)):
            val = it.next(itera2)

            if val['idRuta'] in ruta:
                
                print("Key: " , key, " idruta: ", val['idRuta'], " Promedio :",  val['promedio'] )
                cuenta += val['promedio']
                print("cuneta interna ", cuenta)

        if minimo > cuenta and cuenta != 0:
            print(" Minimo cuenta ", cuenta)
            minimo = cuenta
            cuenta = 0
    
            sale['horario'] = key
            sale['promedio'] = minimo
    
    return sale