import socket
import random
import json
import time


#ayyhaga
# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'  # or '127.0.0.1' to connect to the local machine
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Receive initial message from the server
message = client_socket.recv(1024)
print(message.decode('ascii'))

# Function to receive JSON response from the server
def receive_json_response(client_socket):
    # Receive JSON data from the server
    json_data = client_socket.recv(1024).decode('ascii')
    
    # Decode JSON data
    try:
        response = json.loads(json_data)
        return response
    except json.JSONDecodeError:
        print("Received invalid JSON data from the server:", json_data)
        return None

# Send random numbers between 70 and 100 to the server and receive JSON responses
while True:
    # Generate a random number between 70 and 100
    random_number = random.randint(70, 100)
    
    # Send the random number to the server
    client_socket.send(str(random_number).encode('ascii'))
    
    # Receive JSON response from the server
    response = receive_json_response(client_socket)
    if response:
        print("Received JSON response from the server:")
        print("ID:", response["id"])
        print("Name:", response["name"])
        print("Vital Sign:", response["vitalSign"])
        print("Values:", response["values"])
    
    # Wait for 1 second before sending the next random number
    time.sleep(1)

client_socket.close()
