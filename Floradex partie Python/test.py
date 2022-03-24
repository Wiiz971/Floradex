# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:39:49 2019

@author: El Zorro
"""
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup, UnicodeDammit
from six import u as unicode
from unidecode import unidecode
import os
import time
"""
Consigne : il faut retirer les doubles barres pour pouvoir utiliser 
        a = UnicodeDammit("conserv\xc3\xa9e")

        a.unicode_markup
"""
def recherche():
    dic = {'xc3xa9':'é',
           'xe2x80xa2' : '°',
           'xc3xa0' : 'à',
           'xc3xaa' : 'ê',
           }
    url = 'http://www.tramil.net/fr/plant/abelmoschus-esculentus'
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    paragraphs = re.findall(r'<div class="field field-name-field-plant-prep-poso">(.*?)</div>', str(respData))
    para = paragraphs[0].rstrip()
    cleantext = BeautifulSoup(para, "lxml").text
    a = time.strftime("%a, %d %b %Y, %Hh%Mmin%Ss", time.gmtime())
    with open('%s.txt'%(a),'w') as f:
        f.write(cleantext)
    L=""
    with open('%s.txt'%(a), 'r',encoding = 'utf-8') as fichier:
        while 1:
                data=fichier.readline()
                if not data:
                    break
                L+=data
    #os.remove('text.txt')
    print(L)
    L=L.split('\\') 
    print(L)
    p = ("".join([i for i in L]))
    L1=p.split()
    for i in L1:
        try:
            a=''
            for cle in dic.keys():
                try:
                    i.find(cle)
                    a=cle
                    
                except:
                    pass
            if i in dic.keys():
                i.replace(a,dic[i])
        except:
            pass
    return(" ".join([i for i in L1]))
    
        
    
    

def i(recherche):
    p = recherche()
    clean = UnicodeDammit(p.strip('\\'))
    i = clean.unicode_markup 
    return (i)

"""
for i in L:
    regex = re.compile(r'[\n\r\t]')
    i = regex.sub(" ", i)
    clean = UnicodeDammit(i)
    i = clean.unicode_markup
"""