import smtplib, ssl #se connecter à notre serveur SMTP

from functions_db import *

class GestionEmail():

    def __init__ (self):
        # on rentre les renseignements pris sur le site du fournisseur
        self.smtp_adress = 'smtp.gmail.com'
        self.smtp_port = 465

        # on rentre les informations sur notre adresse e-mail
        self.email_address = 'kassiscarina@gmail.com'
        self.email_password = 'sha*CD25141675'

        # on rentre les informations sur le destinataire
        self.email_receiver = 'kassiscarina@gmail.com'
        print(self.smtp_adress)

    def send_email(self,email_target):        
        self.email_receiver = email_target if len(email_target) != 0 else self.email_receiver
        # on crée la connexion
        context = ssl.create_default_context()
        print(self.smtp_adress)

        #********************** pour creer le contenu html ***********
        var_bdd = ConnectionBDD()
        list_new_annonces = var_bdd.lastAnnonces()
        print(list_new_annonces)
        contenu_email= self.create_contenu(list_new_annonces)
        #********************  **********************
        with smtplib.SMTP_SSL(self.smtp_adress, self.smtp_port, context=context) as server:
            # connexion au compte
            server.login(self.email_address, self.email_password)
            # envoi du mail
            server.sendmail(self.email_address, self.email_receiver, 'Test d envoie d email, VAMOS!!!')
        print('message envoye')
    
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
        <p class ="titre" ></p>
        <p class="lien"> <a href="" target="_blank"> lien à l'annonce</a> </p>        
    </div>
</body>
</html>"""

        return txt_page

