import socket
import threading
import time

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
            if "Question" in message:
                # If the received message contains "Question," it's a quiz question
                answer = input("Your answer: ")
                client_socket.send(answer.encode("utf-8"))
        except socket.error as e:
            print(str(e))
            break

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.238.6", 12222))

# Provide a unique username
username = input("Enter your username: ")
client_socket.send(username.encode("utf-8"))

# Start receiving thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Add a delay to ensure the client has time to connect before the server starts broadcasting questions
time.sleep(2)

# Start an infinite loop to keep the client running
while True:
    pass