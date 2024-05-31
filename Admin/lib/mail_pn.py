
import pandas as pd
from dotenv import load_dotenv
import os
import win32com.client

load_dotenv()

user=os.getenv('user_mail_pn')
password=os.getenv('password_mail_pn')

outlook = win32com.client.Dispatch("outlook.application").GetNamespace("MAPI")

mailbox = outlook.Folders(user)


def extract_data_folder(folder_path, name_file):
    
    folder =    get_folder(mailbox, folder_path)
    if folder:
        messages = folder.Items
        emails_data=[]
        for message in messages:
            try:
                received_time = message.ReceivedTime
                if hasattr(received_time, 'tzinfo') and received_time.tzinfo is not None:
                    received_time = received_time.replace(tzinfo=None)
                        
                    email_data={
                    'ID': message.EntryID if hasattr(message, 'EntryID') else '',
                    'Asunto': message.Subject if hasattr(message, 'Subject') else '',
                    'Remitente': message.SenderName if hasattr(message, 'SenderName') else '',
                    'Email Remitente': message.SenderEmailAddress if hasattr(message, 'SenderEmailAddress') else '',
                    'Cuerpo del mensaje': message.Body if hasattr(message, 'Body') else '',
                    'Adjuntos': message.Attachments.Count if hasattr(message, 'Attachments') else 0,
                    'Recibido el': received_time if hasattr(message, 'ReceivedTime') else '2024/12/31',
                    'Leído': message.Unread if hasattr(message, 'Unread') else '',
                    }
                    emails_data.append(email_data)

            except Exception as e:
                print(f'Ocurrió un error: {e}')
        
        save_df(emails_data, name_file)        

def get_folder(base_folder, folder_path):
    folders = folder_path.split('/')
    folder = base_folder
    try:
        for subfolder in folders:
            folder = folder.Folders[subfolder]
        return folder
    except Exception as e:
        print(f"Error al navegar por las carpetas: {e}")
        return None    

def create_df(message, received_time):
    
    emails_data=[]
    email_data={
    'ID': message.EntryID if hasattr(message, 'EntryID') else '',
    'Asunto': message.Subject if hasattr(message, 'Subject') else '',
    'Remitente': message.SenderName if hasattr(message, 'SenderName') else '',
    'Email Remitente': message.SenderEmailAddress if hasattr(message, 'SenderEmailAddress') else '',
    'Cuerpo del mensaje': message.Body if hasattr(message, 'Body') else '',
    'Adjuntos': message.Attachments.Count if hasattr(message, 'Attachments') else 0,
    'Recibido el': received_time if hasattr(message, 'ReceivedTime') else '2024/12/31',
    'Leído': message.Unread if hasattr(message, 'Unread') else '',
    }
    emails_data.append(email_data)
    return(emails_data)
    

def save_df(emails_data, name_file):
    # Crear un DataFrame a partir de la lista de diccionarios
    df = pd.DataFrame(emails_data)

    # Guardar el DataFrame en un archivo Excel
    name_doc = os.path.join(r"C:\Users\jherrera\Desktop" f"\{name_file}.xlsx")
    print(name_doc)
    df.to_excel(name_doc, index=False)


def view_folder_mail(folder, indent=0):
    print(" " * indent + folder.name)
    for subfolder in folder.Folders:
        view_folder_mail(subfolder, indent + 2)

view_folder_mail(mailbox)
extract_data_folder("Bandeja de entrada/RECLAMACIONES/RENTA_VENTA", 'RENTA_VENTA')