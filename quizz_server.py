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

def handle_client(client_socket, username):
    try:
        while questions:
            current_question = random.choice(questions)
            question_text = current_question['question']
            options = "\n".join(current_question['options'])
            client_socket.send(f'Question: {question_text}\n{options}\n'.encode())

            client_socket.settimeout(10)  # Set a timeout of 5 seconds for client's response
            try:
                client_answer = client_socket.recv(1024).decode().strip().upper()
                correct_answer = current_question['correct_answer']
                if correct_answer == client_answer:
                    scores[username] = scores.get(username, 0) + 1
                    client_socket.send('Correct!\n'.encode())
                else:
                    client_socket.send(f'Wrong Answer! The correct answer is: {correct_answer}\n'.encode())
                if not client_answer:
                    raise socket.timeout
            except socket.timeout:
                client_socket.send("Time's up! Better luck next time.\n".encode())
                continue

            

            client_socket.send(f'Score: {scores.get(username, 0)}\n'.encode())
            questions.remove(current_question)
    except Exception as e:
        print(f'Client {username} disconnected: {e}')
    finally:
        client_socket.close()

host = ''
port = 12222
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
sock.bind((host, port))
sock.listen(3)
print(f"TCP server is listening on {host}:{port}")

while True:
    client, address = sock.accept()
    username = client.recv(1024).decode()
    users[username] = client

    print(f'Accepted connection from {address[0]}:{address[1]} as {username}')
    client_handler = threading.Thread(target=handle_client, args=(client, username))
    client_handler.start()