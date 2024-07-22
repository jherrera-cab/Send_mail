import os
import shutil
import pandas as pd
import re

path_bogota = r'Z:\2. Equipo Bogotá\2.Facturas'
path_cali = r'Z:\3 Equipo Cali\2.Facturas'
path_consolidated = r'Z:\1. Coordinadores\Correos'
pd.set_option('display.max_colwidth', None)

def move_doc():
    
    def extract_cta(nombre):
        match=re.search(r'-(\d+)-', nombre)
        if match:
            return match.group(1)
        else:
            return None
    
    def move_file(path):
        file_origin = os.listdir(path)
        for file in file_origin:
            source_origin = os.path.join(path, file)
            source_destination = os.path.join(path_consolidated, file)
            shutil.move(source_origin, source_destination)
    
    
    move_file(path_bogota)    
    move_file(path_cali)
    
    
    #Creación de Df para manipular la existencia de archivos en la carpeta    
    doc_pendig = os.listdir(path_consolidated)                                #se crea una variable donde se deja todos los nombres de los archivos de la carpeta.
    list_doc_pendig={}                                                  #Nueva variable de tipo lista para dejar la información de formato columna
    for doc in doc_pendig:                                              #Bucle que recorre la lista con todos los nombres crea una lista y luego asigna todos los valores en un DF de pandas
        list_doc_pendig[os.path.join(path_consolidated,doc)]=(extract_cta(doc))
        list_doc_pendig_order=dict(sorted(list_doc_pendig.items()))
  
    
    return list_doc_pendig_order
