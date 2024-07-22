from Admin.connection.Mail.conect_mail import connec_buzon
from Admin.lib.send_mail import send_mail
from Admin.connection.Server.connect_server import create_df
from Admin.lib.move_doc import move_doc
from datetime import datetime
import pandas as pd
import re
import os


conect_server, mail = connec_buzon()

with open('Admin/HTML/plantilla.html', 'r') as file:
    html_template = file.read()

df = create_df()

df.to_excel('data.xlsx', index=False)
date_today=datetime.now().strftime('%d/%m/%Y')

pattern = r'\*(.*?)\*' 
list_doc_pendig = move_doc()
masiv_sinfin = pd.DataFrame(columns=("IDENTIFICACION",	
                                     "GESTOR_ID",	
                                     "HISTORY_DATE",	
                                     'ID_ACCION'	,
                                     'ID_EFECTO'	,
                                     'ID_CONTACTO'	,
                                     'ID_SUBEFECTO'	,
                                     'ID_REACCION'	,
                                     'OBSERVACION'	,
                                     'NEXT_ACTIVITY_DATE'	,
                                     'TELEPHONE'	,
                                     'ACCOUNT_NUMBER',	
                                     'REASON_ID'	,
                                     'EMAIL_ADDRESS',	
                                     'LETTER_ID'	,
                                     'NOMBRE_CONTACTO',	
                                     'STATE_DEBTOR',	
                                     'TEXT1'	,
                                     'TEXT2'	,
                                     'TEXT3'	,
                                     'TEXT4'	,
                                     'TEXT5'	,
                                     'CANAL'))


def update_data(data, file_list, mail_deudor):
    
    sociedad_num = data['sociedad']
    if sociedad_num == '132.0' or sociedad_num == '132':
        sociedad = "NATURGY IBERIA S.A."
        cuenta_bancaria = '2100-0900-91-0211395503'
        swift = 'CAIXESBBXXX'
        iban = 'ES43-2100-0900-9102-1139-5503'
        certificate = r'Z:\1. Coordinadores\2. Jonathan Herrera\Certificaciones bancarias\Naturgy\Certificación Cuenta Bancaria NATURGY IBERIA .S.A.pdf'
        file_list.append(certificate)
    else:
        sociedad = "COMERCIALIZADORA REGULADA, GAS & POWER"
        cuenta_bancaria = '2100-8740-53-0200059831'
        swift = 'CAIXESBBXXX'
        iban =  'ES46.2100.8740.5302.0005.9831'
        certificate = r'Z:\1. Coordinadores\2. Jonathan Herrera\Certificaciones bancarias\Naturgy\DORA REGULADA, GAS Y POWER S.A..pdf'
        file_list.append(certificate)
    
    html_content = html_template    
    html_content = html_content.replace("{{nombre}}",data['nombre'])
    html_content = html_content.replace("{{fecha}}", date_today)
    html_content = html_content.replace("{{cta}}", data['cta'])
    html_content = html_content.replace("{{direccion}}", data['direccion'])
    html_content = html_content.replace("{{Sociedad}}", sociedad)
    html_content = html_content.replace("{{deuda}}", data['deuda'])
    html_content = html_content.replace("{{cta_bancaria}}", cuenta_bancaria)
    html_content = html_content.replace("{{swift}}", swift)
    html_content = html_content.replace("{{iban}}", iban)
    
    
    #send_mail(conect_server, mail, mail_deudor, 'Notificación de Deuda Pendiente y Confirmación de Condiciones de Pago', html_content, file_list)
    
    
def list_file(row):
    for i, list in list_doc_pendig.items() :
        if list == row['ACCOUNT_NUMBER']:
            file_list.append(i)
    return file_list

def create_new_row(row, error):
    if len(error)>0:
        observacion = f'No se hace el envio del correo ya que se encontro error en: {error}, solicitado por: {row['GESTOR_ID']} el dia {row['HISTORY_DATE']}'
    else:
        observacion = f'Se realiza el envio al correo electronico solicitado por: {row['GESTOR_ID']} el dia {row['HISTORY_DATE']}'
        
    if row['ID_EFECTO'] == 'SOLICITUD FACTURA CORREO':
        efecto = 'FACTURA ENVIADA'
    elif row['ID_EFECTO'] == 'TOTAL CORREO' or row['ID_EFECTO'] == 'PARCIAL CORREO':
        efecto = 'ENVIADA CORREO'
        
    new_row = {
            "IDENTIFICACION" : row['IDENTIFICACION'],
            "GESTOR_ID" : 'maquina',
            "HISTORY_DATE":date_today, 
            "ID_ACCION": row['ID_ACCION'],
            "ID_EFECTO": efecto,
            "ID_CONTACTO": 'CONTACTO DIRECTO',
            "ID_SUBEFECTO" : "",
            "ID_REACCION": "",
            "OBSERVACION": observacion, 
            "NEXT_ACTIVITY_DATE": "",
            "TELEPHONE": row['TELEPHONE'], 
            "ACCOUNT_NUMBER":row['ACCOUNT_NUMBER'], 
            "REASON_ID":"",
            "EMAIL_ADDRESS":"",
            "LETTER_ID":"",
            "NOMBRE_CONTACTO":"",
            "STATE_DEBTOR":"",
            "TEXT1":"",
            "TEXT2":"",
            "TEXT3":"",
            "TEXT4":"",	
            "TEXT5":"",
            "CANAL":""
            }
    return new_row
    
for index, row in df.iterrows():
    error = []
    data = {}
    matches = re.findall(pattern, row['OBSERVACION'])
    file_list=[]
    file_list=list_file(row)
    
    if row['ID_EFECTO'] == 'TOTAL CORREO' or row['ID_EFECTO'] == 'SOLICITUD FACTURA CORREO':
        
        if len(matches) == 3:
            mail_deudor = matches[1]
            if len(matches[0]) >= 10:
                data['nombre'] = matches[0]
            else:
                error.append('nombre')
            
            if len(matches[2]) >= 10:
                data['direccion'] = matches[2]
            else:
                error.append('direccion')
            
            data['sociedad'] = row['TEXT1']
            data['deuda'] = row['MONEY1']
            data['cta'] = row['ACCOUNT_NUMBER']
            
        else:
            error.append('observacion') 
    
    elif  row['ID_EFECTO'] == 'PARCIAL CORREO':     
        
        if len(matches) == 4:
            
            mail_deudor = matches[1]
            if len(matches[0]) >= 10:
                data['nombre'] = matches[0]
            else:
                error.append('nombre')
            
            if len(matches[2]) >= 10:
                data['direcccion'] = matches[2]
            else:
                error.append('direccion')
            
            if len(matches[3]):
                data['deuda'] = matches[3]
            else:
                error.append('deuda')
            
            data['cta'] = row['ACCOUNT_NUMBER']
            
        else:
            error.append('observacion')     
    
    
    
    
    if len(error) > 0:
        error_text = ', '.join(error)
        new_row = create_new_row(row, error_text)
    else:
        new_row = create_new_row(row, "")
        
        update_data(data, file_list, mail_deudor)
            
    new_row = pd.DataFrame([new_row])
    masiv_sinfin = pd.concat([masiv_sinfin, new_row], ignore_index=True)
    
day_send_masiv = date_today.replace('/', '')
path_masiv_sinfin = os.path.join(fr'Z:\1. Coordinadores\Correos\Carga sinfin\carga masivo_{day_send_masiv}.xlsx')
masiv_sinfin.to_excel(path_masiv_sinfin, index=False)
        