# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
# Hello World program in Python

#Importation de modules
import sqlite3
import MySQLdb, sys
from dict_app import *


#Dictionnaire d'aplications
class Glob:
    """Espace de noms pour les variables et fonctions <pseudo-globales>"""

    dbName = "FLoradex"      # nom de la base de données
    user = "vincent"              # propriétaire ou utilisateur
    passwd = "abcde"            # mot de passe d'accès
    host = "192.168.0.10"      # nom ou adresse IP du serveur

    # Structure de la base de données.  Dictionnaire des tables & champs :
    dicoT ={"Floradex":[('id_plants', "k", "clé primaire"),
                            ('nom_vernaculaire', 50, "nom vernaculaire"),
                            ('famille', 75, "famille"),
                            ('origine', 75, "origine"),
                            ('espece_endemique', 75, "espece endemique"),
                            ('vertu', 200, "vertu")],
            "Mon_Floradex":[('id-users',"i", "clé primaire")
                        ('id_plants', "k", "clé primaire"),
                        ('nom', 50, "nom"),
                        ('prenom', 50, "prenom"),
                        ('pseudo', 50, "pseudonyme"),
                        ('ville', "i", "ville")],
            "Users":[('id_users', "i", "clé primaire"),
                        ('id_plants', "k", "clé primaire")]}
                        

class GestionBD:

    """Mise en place et interfaçage d'une base de données MySQL"""

    def __init__(self, dbName, user, passwd, host, port =3306):

        "Établissement de la connexion - Création du curseur"

        try:

            self.Floradex = MySQLdb.connect(db =dbName,

                  user =user, passwd =passwd, host =host, port =port)

        except (Exception, err):

            print ('La connexion avec la base de données a échoué :\n'\

                  'Erreur détectée :\n%s' % err)

            self.echec =1

        else:    

            self.cursor = self.Floradex.cursor()   # création du curseur

            self.echec =0


    def creerTables(self, dicTables):

        "Création des tables décrites dans le dictionnaire <dicTables>."

        for table in dicTables:            # parcours des clés du dict.

            req = "CREATE TABLE %s (" % table

            pk =''

            for descr in dicTables[table]:

                nomChamp = descr[0]        # libellé du champ à créer

                tch = descr[1]             # type de champ à créer

                if tch =='i':

                    typeChamp ='INTEGER'

                elif tch =='k':

                    # champ 'clé primaire' (incrémenté automatiquement)

                    typeChamp ='INTEGER AUTO_INCREMENT'   

                    pk = nomChamp

                else:

                    typeChamp ='VARCHAR(%s)' % tch                

                req = req + "%s %s, " % (nomChamp, typeChamp)

            if pk == '':

                req = req[:-2] + ")"

            else:

                req = req + "CONSTRAINT %s_pk PRIMARY KEY(%s))" % (pk, pk)

            self.executerReq(req)


    def supprimerTables(self, dicTables):

        "Suppression de toutes les tables décrites dans <dicTables>"

        for table in dicTables.keys():

            req ="DROP TABLE %s" % table

            self.executerReq(req) 

        self.commit()                       # transfert -> disque


    def executerReq(self, req):

        "Exécution de la requête <req>, avec détection d'erreur éventuelle"

        try:

            self.cursor.execute(req)

        except (Exception, err):

            # afficher la requête et le message d'erreur système :

            print ("Requête SQL incorrecte :\n%s\nErreur détectée :\n%s"\

                   % (req, err))

            return 0

        else:

            return 1


    def resultatReq(self):

        "renvoie le résultat de la requête précédente (un tuple de tuples)"

        return self.cursor.fetchall()


    def commit(self):

        if self.Floradex:

            self.Floradex.commit()         # transfert curseur -> disque        


    def close(self):

        if self.Floradex:

            self.Floradex.close()
            
class Enregistreur:

    """classe pour gérer l'entrée d'enregistrements divers"""

    def __init__(self, bd, table):

        self.bd =bd

        self.table =table

        self.descriptif =Glob.dicoT[table]   # descriptif des champs


    def entrer(self):

        "procédure d'entrée d'un enregistrement entier"

        champs ="("           # ébauche de chaîne pour les noms de champs

        valeurs ="("          # ébauche de chaîne pour les valeurs

        # Demander successivement une valeur pour chaque champ :

        for cha, type, nom in self.descriptif:

            if type =="k":    # on ne demandera pas le n° d'enregistrement

                continue      # à l'utilisateur (numérotation auto.)

            champs = champs + cha + ","

            val = input("Entrez le champ %s :" % nom)

            if type =="i":

                valeurs = valeurs + val +","

            else:

                valeurs = valeurs + "'%s'," % (val)


        champs = champs[:-1] + ")"    # supprimer la dernière virgule,

        valeurs = valeurs[:-1] + ")"  # ajouter une parenthèse

        req ="INSERT INTO %s %s VALUES %s" % (self.table, champs, valeurs)

        self.bd.executerReq(req)


        ch =input("Continuer (O/N) ? ")

        if ch.upper() == "O":

            return 0

        else:

            return 1
            
###### Programme principal : #########


# Création de l'objet-interface avec la base de données : 

bd = GestionBD(Glob.dbName, Glob.user, Glob.passwd, Glob.host)

if bd.echec:

    sys.exit()
 

while 1:

    print ("\nQue voulez-vous faire :\n"\

          "1) Créer les tables de la base de données\n"\

          "2) Supprimer les tables de la base de données ?\n"\

          "3) Entrer des informations sur la flore\n"\

          "4) Entrer des informations sur la flore rencontrée\n"\
              
          "5) Entrer de nouveaux utilisateurs\n"\

          "6) Lister la biliothèque florale\n"\
          
          "7) Lister la bibliothèque sur la flore rencontrée par chaque utilisateur\n"\

          "8) Lister les utilisateurs\n"\

          "9) Exécuter une requête SQL quelconque\n"\

          "10) terminer ?                         Votre choix :",)

    ch = int(input())

    if ch ==1:

        # création de toutes les tables décrites dans le dictionnaire :

        bd.creerTables(Glob.dicoT)

    elif ch ==2:

        # suppression de toutes les tables décrites dans le dictionnaire :

        bd.supprimerTables(Glob.dicoT)     

    elif ch ==3 or ch ==4 or ch==5:

        # création d'un <enregistreur> de Floradex, Mon Floradex ou d'utilisatuers :

        table ={3:'Floradex', 4:'Mon_Floradex', 5:'Users'}[ch]

        enreg =Enregistreur(bd, table)

        while 1:

            if enreg.entrer():

                break

    elif ch ==6 or ch ==7 or ch ==8:

        # listage de toute la biliothèque florale, la bibliothèque sur la flore rencontrée par chaque utilisateur, l'ensemble des utilisateurs

        table ={6:'Floradex', 7:'Mon_Floradex', 8:'Users'}[ch]

        if bd.executerReq("SELECT * FROM %s" % table):

            # analyser le résultat de la requête ci-dessus :

            records = bd.resultatReq()      # ce sera un tuple de tuples

            for rec in records:             # => chaque enregistrement

                for item in rec:            # => chaque champ dans l'enreg.

                    print (item,)

                print

    elif ch ==9:

        req =input("Entrez la requête SQL : ")

        if bd.executerReq(req):

            print (bd.resultatReq())          # ce sera un tuple de tuples

    else:

        bd.commit()

        bd.close()

        break

conn=sqlite3.startup("base de donnees","E:/tipe5/essais/sqlite3")
c = conn.cursor()
c.execute("CREATE table IF NOT EXIST FLORADEX (Genre_nom_latin varchar, Nom_vernaculaire varchar,  Famille varchar, Origine varchar, Vertu varchar, espèce endemique varchar)")
c.execute("INSERT INTO FLORADEX(AGE, NOM, TAILLE) VALUES (15,'Suleau',1.57)")
while 1:
    print ("Veuillez entrer votre requête SQL (ou <Enter> pour terminer) :")
    requete = input()
    if requete =="":
        break
    try:
        c.execute(requete)        # tentative d'exécution de la requête SQL
    except:
        print ('*** Requête incorrecte ***')
    else:    
        print (c.pp())              # affichage du résultat de la requête
    print

choix = input("Confirmez-vous l'enregistrement (o/n) ? ")
if choix[0] == "o" or choix[0] == "O":
    conn.commit()
else:
    conn.close()
