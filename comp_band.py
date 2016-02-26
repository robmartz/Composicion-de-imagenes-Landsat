#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Roberto Martinez.

# ----------------------------------------------------- #
#                                                       #
#  Programa para componer imagenes *.TIF dadas 3 bandas #
#                                                       #
# ----------------------------------------------------- #

try:
    from osgeo import gdal, gdal_array
except:
    sys.exit('[ ERROR ] No se encontro el recurso solicitado: GDAL')
import sys
import numpy as np
import os


def Usage():
    print("""
    EJEMPLO:
    $ python comp_band.py LE70280472015024EDC00_B4.TIF,LE70280472015024EDC00_B1.TIF,LE70280472015024EDC00_B1.TIF salida.TIF
    """)
    sys.exit(1)


def borraTif ( arch_salida ):

    os.system('rm -f ' + arch_salida)


def main( files, output_file ):


    # borra el archivo si existe previamente
    borraTif( output_file )
    
    path = "./data/LE70280472015024EDC00/"
    archivo = files.split(',')
        
    # Se cargan las imagen *.TIF
    infile1 = gdal.Open( path + archivo[0] )
    infile2 = gdal.Open( path + archivo[1] )
    infile3 = gdal.Open( path + archivo[2] )
    
    # Se convierten a arreglos de numpy
    array1 = infile1.ReadAsArray()
    array2 = infile2.ReadAsArray()
    array3 = infile3.ReadAsArray()

    # Se apilan las imagenes
    stacked = np.array( [array1, array2, array3] )
   
    # Escribimos el archivo compuesto de salida 
    gdal_array.SaveArray( stacked.astype("int"), output_file, "GTiff", gdal.Open(path + archivo[0]) )

    
if __name__ == '__main__':

    if len( sys.argv ) < 3:
        print """
        [ ERROR ] Se requieren 2 argumentos de entrada:
        1) Lista de archivos *.TIF separados por comas 
        2) Nombre de archivo de salida 
        """
        Usage()

    main( sys.argv[1], sys.argv[2] )
