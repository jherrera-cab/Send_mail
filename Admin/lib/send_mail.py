import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

def send_mail(server, email, recipient, subject, html_content, file_list):
    
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_content, 'html', 'UTF-8')) 
        
        images= {
            'logo_synerjoy' : 'Admin/HTML/asset/Logo_synerjoy.png',
            'logo_naturgy' : 'Admin/HTML/asset/Logo_naturgy.png'
        }
        
        for(cid, path) in images.items():
            with open(path, 'rb') as img:
                mime = MIMEImage(img.read())
                mime.add_header('Content-ID', f'<{cid}>')
                mime.add_header('Content-Disposition', 'inline', filename=os.path.basename(path))
                msg.attach(mime)
                
                
        if file_list:
            for path in file_list:
                part = MIMEBase('application', 'octet-stream')
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(path)}')
                msg.attach(part)
            
        server.send_message(msg)
        #result = server.sendmail(email, recipient, msg.as_string())

                
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')