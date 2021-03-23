import smtplib, ssl #se connecter à notre serveur SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from functions_db import *

import unidecode
import codecs
import unicodedata

class GestionEmail():

    def __init__ (self):
        self.server = smtplib.SMTP()

        # on rentre les renseignements pris sur le site du fournisseur
        self.smtp_adress = 'smtp.gmail.com'
        self.smtp_port = 465

        # on rentre les informations sur notre adresse e-mail
        self.email_address = 'kassiscarina@gmail.com'
        self.email_password = 'sha*CD25141675'

        # on rentre les informations sur le destinataire
        self.email_receiver = 'kassiscarina@gmail.com'
        print(self.smtp_adress)

    def send_email_html(self,email_target):        
        self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
        print(self.smtp_adress)

        # on crée la connexion
        # server.set_debuglevel(1) # Décommenter pour activer le debug
        self.server.connect(self.smtp_adress)

        self.server.helo() #??
        sujet="Les derniers annonces pour alternance"
        

        #********************** pour creer le contenu html ***********
        var_bdd = ConnectionBDD()
        list_new_annonces = var_bdd.lastAnnonces()
        print(list_new_annonces)
        contenu_email= self.create_contenu(list_new_annonces)
        #********************  **********************

        msg = MIMEMultipart('alternative')
        msg['Subject'] = sujet
        msg['From'] = self.email_address
        msg['To'] = ','.join(self.email_receiver)

        part = MIMEText(contenu_email, 'html')
        msg.attach(part)

        try:
            self.server.sendmail(self.email_address, self.email_receiver, msg.as_string())
            print('message envoye')
            var_bdd.update_anonces_envoye(list_new_annonces)

        except smtplib.SMTPException as e:
            print('ERROR ==>SMTPException :',e)

        """ with smtplib.SMTP_SSL(self.smtp_adress, self.smtp_port, context=context) as server:
            # connexion au compte
            server.login(self.email_address, self.email_password)
            # envoi du mail
            server.sendmail(self.email_address, self.email_receiver, 'Test d envoie d email, VAMOS!!!') """
        
    
    def create_contenu(self, last_annonces):

        txt_page= u"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                </head>
                <body>
                <div>
                        <p class ="titre" >HOLA</p>
                        <p class="lien"> <a href="" target="_blank"> lien à l'annonce</a> </p>        
                    </div>
                </body>
                </html>"""


        return txt_page

    def send_email(self,email_target):        
        self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
        # on crée la connexion
        context = ssl.create_default_context()
        print(self.smtp_adress)

        var_bdd = ConnectionBDD()
        list_new_annonces = var_bdd.lastAnnonces()

        #print(list_new_annonces)
        message=""
        for detaille_annon in list_new_annonces:
            #TypeError: can only concatenate str (not "bytes") to str
            #message +=str("Annonce : "+detaille_annon[1] +"\n").encode('utf-8', errors='ignore') + str(" suivre le lien : "+detaille_annon[8]+"\n\n").encode('utf-8', errors='ignore')
            
            #message +=str("Annonce : "+detaille_annon[1] +"\n").encode('utf-8', errors='ignore') 
            #message +=str(" suivre le lien : "+detaille_annon[8]+"\n").encode('utf-8', errors='ignore')
            message +="Annonce : "+detaille_annon[1] +"\n suivre le lien : "+detaille_annon[8]+"\n\n"
        
        #message=message.decode()# D\xc3\xa9veloppeur
        #message=message.encode() #D\xc3\xa9veloppeur Full Stack H/F
        #message = message.encode('ascii', 'replace').decode('ascii') #D?VELOPPEUR
        #message = unicodedata.normalize("NFKD", message).encode('ASCII', 'ignore')#rien
        #message = unidecode.unidecode(message)
        #message="Hola"#ça marche bien
        #message = unicodedata.normalize("NFD", message)

        """ message=str(list_new_annonces[150][1]).encode('utf-8', errors='ignore')  ça MARCHE !!
        message +=str(" \n "+list_new_annonces[150][8]).encode('utf-8', errors='ignore') """
        message= str(message).encode('utf-8', errors='ignore')
        print(message)
        

        with smtplib.SMTP_SSL(self.smtp_adress, self.smtp_port, context=context) as server:
            # connexion au compte
            server.login(self.email_address, self.email_password)
            # envoi du mail
            server.sendmail(self.email_address, self.email_receiver, message)
        print('message envoye')

