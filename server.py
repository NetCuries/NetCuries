import socket
import threading
import time
import socket
import threading
import time

questions = [
    {'question': 'What is the capital of France?',
     'options': ['A. London', 'B. Berlin', 'C. Paris', 'D. Madrid'],
     'correct_answer': 'C'},

    {'question': 'What is the capital of Tunisia?',
     'options': ['A. London', 'B. Tunis', 'C. Berlin', 'D. Madrid'],
     'correct_answer': 'B'},

    {'question': 'What is the capital of the UK?',
     'options': ['A. London', 'B. Berlin', 'C. Paris', 'D. Madrid'],
     'correct_answer': 'A'},
]

clients = {}
#round_number = 1
max_clients = 2
questions_per_round = 3  # Adjusted to match the number of questions
question_time_limit = 10

def broadcast(username,message):
    for client_data in clients.values():
        if client_data["username"] == username:
            client_socket = client_data["socket"]
            client_socket.send(message.encode("utf-8"))


def broadcast2(message):
    for client_data in clients.values():
        client_socket = client_data["socket"]
        client_socket.send(message.encode("utf-8"))

def handle_client(client_socket, username):
    round_number =1

    # Welcome message
    client_socket.send(f"Welcome to the Quiz, {username}!".encode("utf-8"))

    while True:
        if len(clients) >= max_clients:
            # Start a new round
            broadcast(username,f"\nRound {round_number} is starting!\n")

            # Ask questions
            for question_number, question_data in enumerate(questions):
                question_text = question_data['question']
                options_text = '\n'.join(question_data['options'])
                broadcast(username,f"\nQuestion {question_number + 1}: {question_text}\n{options_text}\n")
                time.sleep(question_time_limit)
                answer=client_socket.recv(1024).decode()
                print(username,answer)    
                clients[username]["answer"]= answer
                # Check if the client answered
                if username in clients and clients[username]["answer"]:
                    if clients[username]["answer"].upper() == question_data['correct_answer']:
                        clients[username]["score"] += 1
                        broadcast(username,f"Correct! {username} gets a point.\n")
                    else:
                        broadcast(username,f"Wrong answer, {username}. The correct answer is {question_data['correct_answer']}.\n")

                    # Reset the answer for the next question
                    clients[username]["answer"] = None
                else:
                    broadcast(username,f"Time's up! The correct answer is {question_data['correct_answer']}.\n")

            # Display individual scores
                broadcast2(f"\n{username}'s score: {clients[username]['score']} points\n")

            # Prepare for the next round
            round_number += 1
            time.sleep(5)  # Wait before starting the next round

# Main function to initialize the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12222))
    server.listen(5)
    print("Server listening on port 8888...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")

        username = client_socket.recv(1024).decode("utf-8")
        clients[username] = {"socket": client_socket, "score": 0, "answer": None,"username":username}

        client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
        client_handler.start()

# Start the server
start_server()


