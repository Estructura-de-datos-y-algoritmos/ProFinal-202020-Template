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

import config as cf
from App import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadFile(analyzer):
    
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadData(analyzer, filename)
    
    model.actualizaPuntos(analyzer)
    model.actulizarRuta(analyzer)
    #model.muestradatos(analyzer)
    return analyzer


def loadData(analyzer, tripFile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    tripFile = cf.data_dir + tripFile
    input_file = csv.DictReader(open(tripFile, encoding="utf-8"),
                                delimiter=",")
    i = 0
    for trip in input_file:
        i = i+1
        model.addTrip(analyzer,trip)
    
    print("totla i***********: ",i)
        
    return analyzer

        
  

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def ordenar(analyzer,valcampo):
    return model.ordenar(analyzer, valcampo)


def puntosPorFecha(analyzer, fecha,numero):
    return model.puntosPorFecha(analyzer, fecha,numero)


def puntosPorRangoFecha(analyzer, fecha1,fecha2, numero):
    return model.puntosPorRangoFecha(analyzer, fecha1,fecha2, numero)


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def minimumCostPath(paths, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(paths, destStation)



def rutasPorRangoHora(analyzer, h_ini,h_fin, ruta):
    return model.rutasPorRangoHora(analyzer, h_ini,h_fin,ruta)