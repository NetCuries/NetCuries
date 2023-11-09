# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:45:11 2023

@author: inesb
"""

from socket import *
import sys
import time 
from threading import Thread
import os
import signal

server_name = '127.0.0.1'
server_port = 12222 #enter the server port

client_socket = socket(AF_INET,SOCK_STREAM)

client_socket.connect((server_name,server_port))

print("Connection to server successful")

#Send the unique username
username = input("username:")
client_socket.send(username.encode())

def inp():
  global start_time,answer
  answer="NO_ANSWER"
  start_time = time.time()
  answer = input("Your answer (A/B/C/D: ")

def timer():
    global t1
    sec = 10
    while True:
        passed = time.time() - start_time
        
        if passed > sec :
            print("Time's up! \n")
            client_socket.send(answer.encode())
            os.kill(t1.ident, signal.SIGINT)  # Send a SIGINT signal to terminate the process



        
while True:
    # Receive the questions and options from the server
    questions_options = client_socket.recv(1024)
    print(questions_options.decode())  
    t2 = Thread(target=timer)
    t1 = Thread(target=inp)
    t1.start()
    t2.start()
    t2.join()
    # Receive the score from the server
    comment = client_socket.recv(1024)
    print(comment.decode())  
    score = client_socket.recv(1024)
    print("The score", score.decode())  # Decode the received score before printing
    

client_socket.close()

