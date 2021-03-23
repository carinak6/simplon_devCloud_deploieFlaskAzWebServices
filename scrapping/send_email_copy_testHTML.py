#coding: utf-8
from io import StringIO  #cStringIO il a disparu
import smtplib, ssl #se connecter à notre serveur SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import email #from email import Charset  #installer pip install charset, ce n'est pas le meme
from email.generator import Generator

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
        #self.email_address = 'kassiscarina@gmail.com'
        self.email_address = [u'Carina é Kassis','kassiscarina@gmail.com']
        self.email_password = 'sha*CD25141675'

        # on rentre les informations sur le destinataire
        #self.email_receiver = 'kassiscarina@gmail.com'
        self.email_receiver = [u'Moi mëme','kassiscarina@gmail.com']
        print(self.smtp_adress)

        self.subject = u'⌘Unicode test⌘'



    def send_email_html(self,email_target):        
        #self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
        print(self.smtp_adress)

        # Default encoding mode set to Quoted Printable. Acts globally!
        #email.charset.add_charset('utf-8', email.charset.CHARSETS.QP, email.charset.CHARSETS.QP, 'utf-8')


        # on crée la connexion
        # server.set_debuglevel(1) # Décommenter pour activer le debug
        self.server.connect(self.smtp_adress)

        #self.server.helo() #??
        #sujet="Les derniers annonces pour alternance"
        

        #********************** pour creer le contenu html ***********
        # var_bdd = ConnectionBDD()
        # list_new_annonces = var_bdd.lastAnnonces()
        # print(list_new_annonces)
        # contenu_email= self.create_contenu(list_new_annonces)
        #********************  **********************

        # Example body
        html = u'Unicode⏎\nTest⏎'
        text = u'Unicode⏎\nTest⏎'

        # 'alternative’ MIME type – HTML and plain text bundled in one e-mail message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "%s" % Header(self.subject, 'utf-8')
        # Only descriptive part of recipient and sender shall be encoded, not the email address
        msg['From'] = "\"%s\" <%s>" % (Header(self.email_address[0], 'utf-8'), self.email_address[1])
        msg['To'] = "\"%s\" <%s>" % (Header(self.email_receiver[0], 'utf-8'), self.email_receiver[1])

       # Attach both parts
        htmlpart = MIMEText(html, 'html', 'UTF-8')
        textpart = MIMEText(text, 'plain', 'UTF-8')
        msg.attach(htmlpart)
        msg.attach(textpart)

        # Create a generator and flatten message object to 'file’
        str_io = StringIO()
        g = Generator(str_io, False)
        g.flatten(msg)
        # str_io.getvalue() contains ready to sent message
        
        # Optionally - send it – using python's smtplib
        # or just use Django's
        s = smtplib.SMTP(self.smtp_adress,self.smtp_port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.email_address, self.email_password)
        s.sendmail("", self.email_receiver[1], str_io.getvalue())
        
    
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
        var_bdd = ConnectionBDD()
        list_new_annonces = var_bdd.lastAnnonces()

        if len(list_new_annonces) !=0:        
            self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
            # on crée la connexion
            context = ssl.create_default_context()
            #print(self.smtp_adress)           

            print('taille des nouveau annonces ',len(list_new_annonces))
            #print('les nouveaux annonces ',list_new_annonces)

            message=""
            if len(list_new_annonces) == 1:
                message =str(list_new_annonces[0][1]).encode('utf-8', errors='ignore')
                message +=str(" \n "+list_new_annonces[0][8]).encode('utf-8', errors='ignore') 
            else:
                for detaille_annon in list_new_annonces:
                    message +="Annonce : "+detaille_annon[1] +"\n suivre le lien : "+detaille_annon[8]+"\n\n"
                       
                message= str(message).encode('utf-8', errors='ignore')
            
            print(message)
            

            with smtplib.SMTP_SSL(self.smtp_adress, self.smtp_port, context=context) as server:
                # connexion au compte
                server.login(self.email_address, self.email_password)
                # envoi du mail
                server.sendmail(self.email_address, self.email_receiver, message)
            print('message envoye')

            print('actualiser les annonces avec la date d\'envoye par email')
            var_bdd.update_anonces_envoye(list_new_annonces) #je l activerai apres
            
            return True
        else:
            print('Pas des nouveaux annonces')
            return False

if __name__ == '__main__':
    #logging.info('%s - logged in successfully', "Appel du main pour la script de scrapping")
    print('ouvre le main')
    test=GestionEmail()
    print('cree l objet gestionemail')  
    print('llama el methodo send_email_html ')
    test.send_email_html('carina')
