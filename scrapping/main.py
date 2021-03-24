import logging
import os

#from scrapping.main import * // a effacer

from scrapping.send_email import *  #scrapping.send_email ==>quand ça tourne sur la VM
from scrapping.scrapping_indeed import *
#from functions_db import *
from scrapping.functions_db_postgres import *
from scrapping.service_cleanBDD_PG import *

#pour savoir l'adresse du fichier et l'utiliser dans le crontab 
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path,'main.py')
print(filename)

logging.basicConfig(filename='logging_scrapping.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def main(compte_email): 
    logging.info('Beginning of the script')  
    print('entra à main') 
    logging.info('creation de l\'instance de la classe indeed')
    var_indeed = Indeed()

    logging.info('on execute les processus pour obtenir les informations sur le site indeed - Start')
    var_tuples = var_indeed.generateur_tuples()
    #print(var_tuples)
    logging.info('Les donnes trouvés on genere les suivant touples : '+str(var_tuples))
    logging.info('on execute les processus pour obtenir les informations sur le site indeed - End')

    logging.info('on cree une instance de la classe conn_bd que realise la connexion avec la BDD - Start')
    var_donnes= ConnectionBDD_PG()
    var_donnes.create_table_offer()
    logging.info('J\'execute la methode enregistrer_donnes qui prends les tuples generé avant - Start')
    var_donnes.enregistrer_donnes(var_tuples)
    logging.info('je recupere les donnes pour enregistre dans la BDD - Start')
    donnes = var_donnes.afficher_donnes()
    #print(donnes)
    logging.info('je recupere les donnes pour enregistre dans la BDD : '+ str(donnes) +' - End')
    logging.info('J\'execute la methode enregistrer_donnes qui prends les tuples generé avant - End')
    logging.info('On cree une instance de la classe conn_bd que realise la connexion avec la BDD - End')

    logging.info('On cree une instance de la classe CleanBdd que realise le netoyage de la BDD - Start')    
    clean_bdd = CleanBdd_PG()
    reponse =clean_bdd.clean_bdd()
    print(reponse)
    logging.info('On cree une instance de la classe CleanBdd que realise le netoyage de la BDD - Fin : '+reponse) 
    
    logging.info('On cree une instance de la classe GestionEmail que realise l\'envoye de l\'email - Start') 
    var_email = GestionEmail() #on instance la classe d envoie email
    email_target=compte_email #'kassiscarina@gmail.com'
    reponse_email=var_email.send_email(email_target)
    
    
    print('fin message envoye')
    logging.info('On cree une instance de la classe GestionEmail que realise l\'envoye de l\'email - End : '+email_target) 
    
    logging.info('Fin du main') 
    return reponse_email

if __name__ == '__main__':
    logging.info('%s - logged in successfully', "Appel du main pour la script de scrapping")
    reponse_main=main()
    print('reponse pour send email'+reponse_main)

