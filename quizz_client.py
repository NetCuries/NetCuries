from socket import *
import keyboard
import sys
import time 
from threading import Thread
import os
import signal

server_name = '127.0.0.1'
server_port = 12222 

client_socket = socket(AF_INET,SOCK_STREAM)

client_socket.connect((server_name,server_port))

print("Connection to server successful")

username = input("username:")
client_socket.send(username.encode())

def press_enter():
    time.sleep(10)
    answer = "NO_ANSWER"  
    keyboard.press_and_release('enter')

def get_user_input():
    global answer
    answer = input("Please enter something: ")

    
while True:
    global answer
    answer="NO_ANSWER"
    questions_options = client_socket.recv(1024)
    print(questions_options.decode()) 
    press_thread = Thread(target=press_enter)
    get_input_thread = Thread(target=get_user_input)
    press_thread.start()
    get_input_thread.start()
    press_thread.join()
    get_input_thread.join()
    client_socket.send(answer.encode())
    comment = client_socket.recv(1024)
    print('Wrong Answer! \n The correct answer is ',comment.decode(),' \n')  
    score = client_socket.recv(1024)
    print("The score", score.decode())  
    

client_socket.close()