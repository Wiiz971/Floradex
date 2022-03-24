# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 20:10:12 2018

@author: El Zorro
"""

##### PROGRAMME PRINCIPAL #####

import sqlite3
import time

with sqlite3.connect("H:\tipe5\Floradex.mwb") as db:
    c = db.cursor()
c.execute("""
          CREATE TABLE IF NOT EXISTS Users(
          userID INTEGER PRIMARY KEY,
          username VARCHAR(20) NOT NULL,
          firstname VARCHAR(20) NOT NULL,
          surname VARCHAR(20) NOT NULL,
          password VARCHAR(20) NOT NULL),
          """)
c.execute("""
          INSERT INTO Users(username,fisrtname,surname,password) VALUES ("AZINCOURT","VINCENT","Wiiz","22112k7b")
          """)
db.commit
c.execute("SELECT * FROM Users")
print(c.fetchall())

def login():
    while True:
        username= input("Veuillez entrer votre nom d'utilisateur")
        password=input("Veuillez entrer votre mot de passe")
        with sqlite3.connect("MonFloradex.db") as db:
            cursor=db.cursor()
        find_user=("SELECT * FROM Users WHERE username= ? AND password = ?")
        cursor.execute(find_user,(username),(password))
        results = cursor.fetchall()
        
        if results:
            for i in results:
                print("Welcome"+i[2])
            #return ("exit")
            break
        
    else:
        print("Nom d'utilisateur et mot de masse incorrect")
        again = input ("Voulez-vous réésayer ?(o/n),")
        if again.lower()== "n":
            print("Goodbye")
            time.sleep(1)
            return("break")
        
  
login()

            
        
        