# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:45:11 2023

@author: inesb
"""

from socket import *
import threading

def listen_for_questions():
    while True:
        
        #welcome message
        welcome = client_socket.recv(1024).decode()
        print(welcome)
        
        # Receive a question from the server
        questions_options = client_socket.recv(1024).decode()
        print(questions_options)

        # Get the user's answer
        answer = input("Enter you answer: \n")

        # Send the user's answer to the server
        client_socket.send(answer.encode())

        # Receive correct answer from the server 
        correct_answer = client_socket.recv(1024).decode()
        print(correct_answer)
            
server_name = "192.168.1.192"
server_port = 12222 #enter the server port

client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_name,server_port))

print("Connection to server successful")

#Send the unique username to the server
username = input("username:")
client_socket.send(username.encode())

# Start a new thread to listen for questions from the server
thread = threading.Thread(target=listen_for_questions)
thread.start()
client_socket.close()




