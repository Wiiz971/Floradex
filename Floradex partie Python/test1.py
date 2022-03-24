# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:18:17 2019

@author: El Zorro
"""
import socket
tempsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tempsocket.bind(("127.0.0.1", 45678))   ## Tuple: (IP Addr, Port)
tempsocket.listen(1)
conn, addr = tempsocket.accept()        ## Listener blocks here awaiting sender's connect()
conn.recv(1024).decode('UTF-8')

#https://stackoverflow.com/questions/48266026/socket-java-client-python-server