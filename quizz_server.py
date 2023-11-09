import socket
import time
import random
import threading


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

clients = []
scores = {}
host = ''
port = 12222
time_limit = 30


            
def handle_client(client):
    username = client.recv(1024).decode()
    client.send("Welcome to the quiz game, {}!".format(username).encode())
    
    #Maximum 3 clients need to connect
    #while len(clients) < 3:
           # pass
        
    #choose the question and its related answer
    current_question = random.choice(questions)
    print("cur",current_question)
    question_text = current_question['question']
    options = "\n".join(current_question['options'])
    correct_answer = current_question['correct_answer']
    
    #Display the questions to all clients
    for client in clients:
        client.send(f'Question: {question_text}\n{options}\n'.encode())
        
    # Start a timer for the current question
    timer = threading.Timer(time_limit, correct_answer)
    timer.start()
    
    while True:
        #check if the client answered
        answer = client.recv(1024).decode()
        if answer == correct_answer:
            timer.cancel()
            scores[username] = scores.get(username, 0) + 1
            
            #Display to all clients the correct answer
            for client in clients:
                client.send(correct_answer.encode())
            break
        
        #close the client connection
        client.close()
        


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
sock.bind((host, port))
sock.listen(3)
print(f"TCP server is listening on {host}:{port}")



while True:
    client, address = sock.accept()
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
