import socket
import cv2


def start_server():
    # Define the host and port to listen on
    host = "127.0.0.1"  # Use "0.0.0.0" to accept connections from any IP
    port = 12345

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified host and port
    server_socket.bind((host, port))

    # Listen for incoming connections (maximum of 5)
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}...")

    while True:
        # Accept a new incoming connection
        client_socket, client_address = server_socket.accept()

        print(f"Accepted connection from {client_address}")

        # Start a new thread to handle the client
        client_handler = ClientHandler(client_socket)
        client_handler.start()

class ClientHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def start(self):
        # Handle the client in a loop
        while True:
            # Receive data from the client
            data = self.client_socket.recv(1024)


            if not data:
                # If no data is received, the client has closed the connection
                print("Connection closed by client.")
                break

            # Echo the received data back to the client
            self.client_socket.sendall(frame)

        # Close the client socket
        self.client_socket.close()

