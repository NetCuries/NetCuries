# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:45:11 2023

@author: inesb
"""

from socket import *
import sys
import select

server_name = "192.168.50.147"
server_port = 12222 #enter the server port

client_socket = socket(AF_INET,SOCK_STREAM)

client_socket.connect((server_name,server_port))

print("Connection to server successful")

#Send the unique username
username = input("username:")
client_socket.send(username.encode())


while True:
    # Receive the questions and options from the server
    questions_options = client_socket.recv(1024)
    print(questions_options.decode())  
    
    answer = input()
    # Receive the score from the server
    score = client_socket.recv(1024)
    print("The score", score.decode())  # Decode the received score before printing
    

client_socket.close()

