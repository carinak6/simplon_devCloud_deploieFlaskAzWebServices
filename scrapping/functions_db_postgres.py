import requests
import pprint

import datetime

import psycopg2

class ConnectionBDD_PG:
    def __init__(self):
        #, dbName, user, passwd, host
        #"Établissement de la connexion - Création du curseur"
        try: 
            
            #docker run -it --rm postgres psql -h carina-bddscrapping.postgres.database.azure.com -U caryk6@carina-bddscrapping -p 5432 postgres
            #self.cnx = psycopg2.connect(host ='localhost', user ='postgres', dbname ='postgres', password ='cba1491EPINAY', sslmode = 'require') , port= '5432'
            self.cnx = psycopg2.connect(host ='40.84.54.98', user ='postgres', dbname ='postgres', password ='cba1491EPINAY',sslmode = 'require')

            print('connexion reussi PostGresql!!!') 
            #self.mycursor = self.cnx.cursor()
            self.echec =0

        except (Exception, psycopg2.Error) as error :
            print("Something went wrong, La connexion avec la base de données a échoué : "+str(error))       
            self.echec =1 
    
    def create_table_offer(self):
        mon_curseur = self.cnx.cursor()
        mon_curseur.execute("CREATE TABLE IF NOT EXISTS offer (offer_id SERIAL, titre VARCHAR(200) NOT NULL, description TEXT NOT NULL, date_offre TEXT, salaire VARCHAR(100), localisation VARCHAR(200), id_entreprise INT, date_current DATE, lien TEXT NULL, date_send_email DATE NULL)")
        self.cnx.commit() #valide la transaction
        print('creation reussi create_table_offer !!!')

        """  a jouter, pour le liverer les recours
        cur.close()
        conn.close()
        print("La connexion PostgreSQL est fermée") """
         
    def create_tables(self):
        mon_curseur = self.cnx.cursor()
        mon_curseur.execute("CREATE TABLE offer (offer_id INTEGER AUTO_INCREMENT PRIMARY KEY, titre VARCHAR(200) NOT NULL, description TEXT NOT NULL, date_offre TEXT, salaire VARCHAR(100), localisation VARCHAR(200), id_entreprise INT, date_current DATE, lien TEXT NULL, date_send_email DATE NULL)")
        mon_curseur.execute("CREATE TABLE entreprise (id_entreprise INTEGER AUTO_INCREMENT PRIMARY KEY, nom_entreprise VARCHAR(200) NOT NULL, adresse TEXT NULL, code_postal VARCHAR(10))")    
        
        self.cnx.commit() #valide la transaction
        print('creation reussi des tables offer et entreprise!!!')

    def enregistrer_donnes(self,donnes):
        
        try:
            mon_cursor = self.cnx.cursor()
            #print(donnes)           

            #on cree la requete d'insertion
            sql_insert = ('INSERT INTO offer(titre, description,date_offre,salaire,localisation,id_entreprise, date_current, lien) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)')
            
            #on execute le methode pour inserer les donnes sur la BDD bd_scrapping)
            mon_cursor.executemany(sql_insert, donnes) #execute le curseur avec la methode executemany transmit la requete
            
            self.cnx.commit() #valide la transaction
                
            print(mon_cursor.rowcount, "record inserted.\n")           


        except (Exception, psycopg2.Error) as error:
            print("Something went wrong, un erreur se produit : {}".format(error))

    def effacer_tous_annonces(self):
        
        try:
            mon_cursor = self.cnx.cursor()

            sql = "DELETE FROM offer"
            mon_cursor.execute(sql)

        except (Exception, psycopg2.Error) as error:
            print("Something went wrong, un erreur se produit : {}".format(error))


    def afficher_donnes(self):

        try:
            mon_cursor = self.cnx.cursor()

            mon_cursor.execute('SELECT * FROM offer')
            res = mon_cursor.fetchall()
            
            self.liste_donnes_offer=[]
            for line in res:
                #print(line)
                self.liste_donnes_offer.append(line)

            return self.liste_donnes_offer  

        except(Exception, psycopg2.Error) as error:
            print("Something went wrong, un erreur se produit : {}".format(error))
    
    def lastAnnonces(self):
        #il faudra verifier avec le dernier annonce en BDD si il y a eu des nouveaux
        try:
            mon_cursor = self.cnx.cursor()
            annonces_non_send=[]
            print('************* lastAnnonces ***************')
            mon_cursor.execute('SELECT * FROM offer WHERE date_send_email IS NULL')
            #mon_cursor.execute('SELECT * FROM offer LIMIT 3 OFFSET 3')
            print('SELECT * FROM offer LIMIT 3 OFFSET 3')
            annonces_non_send = mon_cursor.fetchall()
            
            # self.liste_donnes_offer=[]
            # for line in res:
            #     #print(line)
            #     self.liste_donnes_offer.append(line)
            print(annonces_non_send)
            return annonces_non_send  

        except (Exception, psycopg2.Error) as error:
            print("Something went wrong, un erreur se produit : {}".format(error))

    def update_anonces_envoye(self, liste_annonces):
        try:
            mon_cursor = self.cnx.cursor()
            #print(liste_annonces)           

            for annonce in liste_annonces:
                #on cree la requete d'update
                #print(annonce)
                sql_update = f'UPDATE offer SET date_send_email = NOW() WHERE offer_id = {annonce[0]}'
                print(sql_update)

                #on execute le methode pour inserer les donnes sur la BDD bd_scrapping)
                mon_cursor.execute(sql_update) #execute le curseur avec la methode executemany transmit la requete
                print(mon_cursor.rowcount, "record updated.\n") 

            self.cnx.commit() #valide la transaction
                
                      
            print('Actualisation des données avec la date d envoie des annonces, END')
            return True

        except (Exception, psycopg2.Error) as error:
            print("Something went wrong, un erreur se produit : {}".format(error))

""" if __name__ == '__main__':
    #logging.info('%s - logged in successfully', "Appel du main pour la script de scrapping")
    print('pret!!!')
    inst_bdd = ConnectionBDD_PG()
    print(inst_bdd.afficher_donnes() ) """
