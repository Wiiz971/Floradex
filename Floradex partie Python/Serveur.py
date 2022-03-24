# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:04:27 2019

@author: El Zorro
"""

 ########################### IMPORTATION DE MODULES ###########################
import json
import requests
import socket
import threading
import sqlite3
import http.server
import string
import urllib.error
import urllib.request
import urllib.parse
import urllib3
import re
from bs4 import BeautifulSoup
import panda as pd
import numpy as np
########################### Importation d'une table ###########################

Lascii=string.ascii_uppercase
DIGITS = string.digits

 ################################ API KEYS ####################################
KeyPlantnet="2a10BNtywoBeNpeXTpZzTmG3z"
KeyYandexTranslate="trnsl.1.1.20190304T213103Z.2574840aa0ae003b.f987b8431d5442374b70b9d4745ab9599afd87fa"

 ################# DEFINITION CLASSES CONNEXION/RECHERCHE #####################
class recherche():
    def __init__(self,plantes,LatinName):
        self.plantes = plantes
        self.LatinName = LatinName
    def request_Phytotherapie(self): #Recherche sur le site Vulgaris
        """exemple : https://www.vulgaris-medical.com/phytotherapie/bacopa-monnier"""
        for char in self.plantes:
            if char in " _+%":
                self.plantes = self.plantes.replace(char,'-')
        url = 'https://www.vulgaris-medical.com/phytotherapie/%s'%(self.plantes)
        try:
            htt = urllib3.PoolManager()
            data = htt.request('GET', url)
            page = data.data.decode('utf-8')[2:]
            soup = BeautifulSoup(page, 'lxml')
            a = soup.find_all('div', class_="field field-name-body field-type-text-with-summary field-label-hidden")
            M = str(a[0])
            L = re.sub('<[^<]+?>', '',M)
            o = L.find('.')
            L=L[o+2:]
            regex = re.compile(r'[\n\r\t\xa0]')
            L = regex.sub(" ", L)
            return L 
        except urllib3.error.HTTPError as e:
            print('Le serveur ne pouvait pas répondre à la requête.')
            print('Error code: ', e.code)
        except urllib3.error.URLError as e:
            print("Nous n'avons pas réussi à parvenir à un serveur.")
            print('Reason: ', e.reason)
        else:
            # everything is fine wap wap
            next
    def request_Phytotherapie2(self): # recherche sur Plants For a Future
        """exemple : https://pfaf.org/user/Plant.aspx?LatinName=Casimiroa+edulis"""
        for char in self.LatinName:
            if char in " _-%":
                self.LatinName = self.LatinName.replace(char,'+')
        url= 'https://pfaf.org/user/Plant.aspx?LatinName=%s'%(self.LatinName)
        try:
            htt = urllib3.PoolManager()
            data = htt.request('GET', url)
            page = data.data.decode('utf-8')[2:]
            soup = BeautifulSoup(page, 'lxml')
            a = soup.find_all('span', id='ctl00_ContentPlaceHolder1_txtMediUses')
            M = str(a[0])
            L = re.sub('<[^<]+?>', '',M) #Pour retirer les balises
            Li ="".join([i for i in L])
            a=0
            while a !=-1:
                a = Li.find('[')
                Li = Li[:a]+Li[a+8:]
            Mots=translater('%s'%Li)
            regex = re.compile(r'[\n\r\t\xa0]')
            Mots = regex.sub(" ", Mots)
            return Mots
        except urllib3.error.HTTPError as e:
            print('Le serveur ne pouvait pas répondre à la requête.')
            print('Error code: ', e.code)
        except urllib3.error.URLError as e:
            print("Nous n'avons pas réussi à parvenir à un serveur.")
            print('Reason: ', e.reason)
        else:
            # everything is fine wap wap
            next
    def request_pythotherapie3(self): #Recherche sur le site TRAMIL
        """ exemple : http://www.tramil.net/fr/plant/abelmoschus-esculentus"""
        for char in self.LatinName:
            if char in " _+%":
                self.LatinName = self.LatinName.replace(char,'-')
        url = 'http://www.tramil.net/fr/plant/%s'%(self.LatinName)
        try:
            htt = urllib3.PoolManager()
            data = htt.request('GET', url)
            page = data.data.decode('utf-8')[2:]
            soup = BeautifulSoup(page, 'lxml')
            a = soup.find_all('div', class_='field field-name-field-plant-prep-poso')
            M = str(a[0])
            L = re.sub('<[^<]+?>', '',M)
            regex = re.compile(r'[\n\r\t\xa0]')
            L = regex.sub(" ", L)
            return L
        except urllib3.error.HTTPError as e:
            print('Le serveur ne pouvait pas répondre à la requête.')
            print('Error code: ', e.code)
        except urllib3.error.URLError as e:
            print("Nous n'avons pas réussi à parvenir à un serveur.")
            print('Reason: ', e.reason)
        else:
            # everything is fine wap wap
            next        
class ClientThread(threading.Thread,recherche):
    def __init__(self,ip,port,clientsocket):
         threading.Thread.__init__(self)
         self.ip = ip
         self.port = port
         self.clientsocket = clientsocket
         print("[+] Nouveau thread pour %s %s "%(self.ip,self.port))
    def run(self):
        print("Connexion de %s %s"%(self.ip, self.port))
        URLImage=self.clientsocket.recv(2048)#1 seul argument
        print(URLImage)
        URLImage=URLImage[1:]
        print("Traitement de l'image...")
        fp = researcher_phytotherapie(URLImage,'Citron')#SEND_API_Plantnet(URLImage)
        with open('%s.txt'%self.ip , "w") as fichier:
            fichier.write("%s"%fp)
        file=open('%s.txt'%self.ip,'rb')
        self.clientsocket.send(file.read())
        file.close()
        print("Client déconnecté...")

 ####################### Envoi a l'API YandexTranslate/SyStran ########################        
def translater(chaine):
    for i in chaine:
        for char in i:
            if char in " ":
                i = i.replace(char,'%')
    response = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20190304T213103Z.2574840aa0ae003b.f987b8431d5442374b70b9d4745ab9599afd87fa&text=%s&lang=fr&[format=<text plain>]"%(chaine))
    texte=response.text
    L=[i for i in texte.split()]
    EN=[L[0][36:]]
    z=ord('z')
    A=ord('A')
    ORD=[ord('é'),ord('è'),ord('à'),ord('ù'),ord('â'),ord('ê'),ord('î'),ord('ô'),ord('û'),ord(' '),ord(','),ord('!'),ord('?'),ord('('),ord(')'),ord("'"),ord('.')]
    for j in L[1:]:
        for char in j:
            if ((ord(char)>=z and ord(char)<=A) or (ord(char) not in ORD)):
                j = j.replace(char,'')
    for i in L[1:]:
        EN.append(i)
    EN[-1]=EN[-1][:-3]
    s=" ".join([i for i in EN])
    return s

 ########################## ENVOI A L'API PL@NTNET ############################

def SEND_API_Plantnet(URLImage,organs):
    global KeyPlantnet
    url = "https://my-api.plantnet.org/v1/identify/all?images=%s&organs=%s&lang=fr&api-key=%s"%(URLImage,organs,KeyPlantnet)
    json_data = {"siteUrl": "https://plantnet.org"}
    r = requests.post(url, json=json_data)
    a = r.text
    with open(r'"\home\pi\Documents\Database_Floradex\%s.txt"'%URLImage , "w") as fichier:
        fichier.write("%s"%a)    
    return a
 ######################### DataBase SQLite in Python ##########################
"""
db=sqlite3.connect('/home/pi/Bureau/Floradex.db')
try:

    cursor=db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY, name TINYTEXT, email VARCHAR(50) unique, password TEXT unique, URLImage LONGTEXT, recherches LONGTEXT, edit TIMESTAMP(14) )''')
    db.commit()
except Exception as e:
    db.rollback()
    raise e
finally:    
    db.close() #Close the database connection
    

def add(URL):
    db=sqlite3.connect('/home/pi/Bureau/Floradex.db')
    try:
        cursor=db.cursor()
        sql="INSERT INTO Users(URLImage,edit) VALUES('%s',NOW())"%URL
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:    
        db.close() #Close the database connection
"""
 ############################ PROGRAMME PRINCIPAL #############################
                ############# SERVEUR RASPBERRY PI #############
"""
SENDING IMAGE FROM ANDROID TO PC WITH TCP METHOD
"""
"""
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    clientsocket, (ip, port)= tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
"""
"""
REPONSE JSON DE LA FORME:
    
{
  "query": {
    "project": "string",
    "images": [
      "string"
    ],
    "organs": [
      "string"
    ]
  },
  "language": "string",
  "preferedReferential": "string",
  "results": [
    {
      "score": 0,
      "species": {
        "scientificNameWithoutAuthor": "string",
        "scientificNameAuthorship": "string",
        "genus": {
          "scientificNameWithoutAuthor": "string",
          "scientificNameAuthorship": "string"
        },
        "family": {
          "scientificNameWithoutAuthor": "string",
          "scientificNameAuthorship": "string"
        },
        "commonNames": [
          "string"
        ]
      },
      "images": [
        {
          "url": "string",
          "organ": "string"
        }
      ]
    }
  ]
}
  
Autre test    
for char in plante:
                if char in " -":
                    plante = plante.replace(char,'_')
            ra = requests.get('https://practicalplants.org/wiki/%s'%(plante))
            text = ra.text
            M=[j for j in text.split()]
            toxic=M.index('id="Toxic_parts">Toxic')
            toxic = Toxic+5
            Toxic=M[toxic:]
            S=['Toxic Part']
            medic=M.index('href="/wiki/Medicinal_uses"')
            medic=Medic+6
            Medic=M[medic:]
"""
    
