import socket
import time 
import random
import threading 

users = {}
questions = [
    {'question': 'What is the capital of France?',
     'options': ['A. London', 'B. Berlin', 'C. Paris', 'D. Madrid'],
     'correct_answer': 'C'},
    
    {'question': 'What is the capital of Tunisia?',
     'options': ['A. London', 'B. Tunis', 'C. Berlin', 'D. Madrid'],
     'correct_answer': 'B'},
    
    {'question': 'What is the capital of UK?',
     'options': ['A. London', 'B. Berlin', 'C. Paris', 'D. Madrid'],
     'correct_answer': 'A'},
]
scores = {}

def handle_client(client_socket,username):
    try:
        while questions:
            current_question=random.choice(questions)
            question_text=current_question['question']
            options="\n".join(current_question['options'])
            client_socket.send(f'Question: {question_text}\n{options}\n'.encode())
            client_answer = client_socket.recv(1024).decode().strip().upper()
            print(client_answer)
            if client_answer != "":
                correct_answer = current_question['correct_answer']
                if correct_answer == client_answer:
                    scores[username]=scores.get(username,0)+1
                    client_socket.send('Correct! \n'.encode())
                else:
                     client_socket.send('Wrong Answer! \n The correct answer is : {correct_answer}\n'.encode())
            else:
                client_socket.send("time over! better luck next time.\n".encode())

            client_socket.send(f'Score: {scores.get(username, 0)}\n'.encode())
            questions.remove(current_question)
           
    except Exception as e: 
        print(f'Client {username} disconnected: {e}')
        client_socket.close()


host = ''
port = 12222
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP 
sock.bind((host,port))
sock.listen(3)
print(f"UDP server is listening on {host}:{port}")

while True:
    
    client,address =sock.accept()
    username=client.recv(1024).decode()
    users[username]=client

    print(f'Accepted connection from {address[0]}:{address[1]} as {username}')
    client_handler=threading.Thread(target=handle_client,args=(client, username))
    client_handler.start()
