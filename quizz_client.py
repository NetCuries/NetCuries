# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:45:11 2023

@author: inesb
"""
import keyboard
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
    global answer
    answer="NO_ANSWER"
    prompt = input("Your answer (A/B/C/D) : \n")
    if prompt in ["A","B","C","D"] : answer = prompt

def timer():
    global timeup 
    timeup = False
    time.sleep(10)
    if (answer =="NO_ANSWER") :
       print("Time's up! \n")
       timeup = True
       keyboard.press_and_release('enter')

    
while True:
    global answer
    answer="NO_ANSWER"
    # Receive the questions and options from the server
    questions_options = client_socket.recv(1024)
    print(questions_options.decode())  
    t2 = Thread(target=timer ,daemon=True)
    t2.start()
    prompt = input("Your answer (A/B/C/D) : \n")
    if prompt in ["A","B","C","D"] and not timeup : answer = prompt
    t2.join()
    client_socket.send(answer.encode())
    # Receive the score from the server
    comment = client_socket.recv(1024)
    print(comment.decode())  
    score = client_socket.recv(1024)
    print(score.decode())  # Decode the received score before printing
    

client_socket.close()

