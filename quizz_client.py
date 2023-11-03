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

threading.Thread(target=receive_messages, args=(client, text_widget), daemon=True).start()


import threading
import sys
import time

# Global variable to store the user's answer
user_answer = None

# Function to get user input
def get_user_input():
    global user_answer
    user_answer = input("Your answer: ")

# Function to handle timer
def timer():
    global user_answer
    time.sleep(30)  # Wait for 30 seconds
    if user_answer is None:
        user_answer = "No answer provided within the time limit."

# Main function to receive and process questions
def receive_question():
    while True:
        question = client.recv(1024).decode()
        if not question:
            break
        print(f"Question: {question}")

        # Start the timer and prompt user for answer
        timer_thread = threading.Thread(target=timer)
        timer_thread.start()
        get_user_input()

        # Wait for the timer thread to finish (maximum 30 seconds)
        timer_thread.join()

        # Send user's answer to the server
        client.send(user_answer.encode())

        # Receive and print feedback from the server
        feedback = client.recv(1024).decode()
        print(feedback)
