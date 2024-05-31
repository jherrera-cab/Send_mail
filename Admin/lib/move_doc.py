import os
import shutil
import pandas as pd
import re

path_bogota = r'Z:\2. Equipo Bogotá\2.Facturas'
path_cali = r'Z:\3 Equipo Cali\2.Facturas'
path_consol = r'Z:\1. Coordinadores\Masivos\Facturas\Pendientes'
pd.set_option('display.max_colwidth', None)

def move_doc():
    
    def extract_cta(nombre):
        match=re.search(r'\d+(?=[\s_]*[\-_])', nombre)
        if match:
            return match.group()
        else:
            return None
        
    doc_bogota = os.listdir(path_bogota)
    for doc in doc_bogota:
        sourse_bogota = os.path.join(path_bogota, doc)
        destination = os.path.join(path_consol, doc)
        shutil.move(sourse_bogota, destination)
        
    doc_cali=os.listdir(path_cali)
    for doc in doc_cali:
        destination = os.path.join(path_consol, doc)
        sourse_cali = os.path.join(path_cali, doc)
        shutil.move(sourse_cali, destination)
    
    #Creación de Df para manipular la existencia de archivos en la carpeta    
    doc_pendig = os.listdir(path_consol)                                #se crea una variable donde se deja todos los nombres de los archivos de la carpeta.
    list_doc_pendig=[]                                                  #Nueva variable de tipo lista para dejar la información de formato columna
    for doc in doc_pendig:                                              #Bucle que recorre la lista con todos los nombres crea una lista y luego asigna todos los valores en un DF de pandas
        name_doc=os.path.join(path_consol, doc)
        list_doc_pendig.append(name_doc)
        df_list_doc=pd.DataFrame(list_doc_pendig, columns=['name'])
        df_list_doc['Cta'] = df_list_doc['name'].apply(extract_cta)     #Se utiliza una funcion para con expresiones regulares extraer la cuenta contrato del nombre que esta entre "-"
        df_remove_doc = df_list_doc[(df_list_doc['Cta'].str.len()<=4) | (pd.isna(df_list_doc['Cta']))]
        
  

    if len(df_remove_doc)>0:
        for index, row in df_remove_doc.iterrows():
            file_name=row['name']
            os.remove(file_name)
        print(f'Se elimino de la carpeta {len(df_remove_doc)} archivos por error en el nombre.')
    else:
        print('No se hace limpieza de la carpeta por el nombre del documento.')
    
    df_merg_file = pd.merge(df_list_doc,df_remove_doc, on='Cta', how='inner')
    indices_a_eliminar = df_merg_file.index.tolist()
    df_clean = df_list_doc.drop(indices_a_eliminar)    


move_doc()