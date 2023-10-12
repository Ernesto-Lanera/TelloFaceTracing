import threading
import socket
from djitellopy import Tello
import cv2
import keyboard

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, tello):
        super().__init__()
        self.client_socket = client_socket
        self.tello = tello

    def run(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                print("Connection closed by client.")
                break

            # Process client commands
            command = data.decode()
            if command == "takeoff":
                self.tello.takeoff()
            elif command == "land":
                self.tello.land()
            elif command == "streamon":
                self.tello.streamon()
            elif command == "streamoff":
                self.tello.streamoff()
            else:
                print("Unknown command:", command)

        self.client_socket.close()

def start_server(tello):
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
        client_handler = ClientHandler(client_socket, tello)
        client_handler.start()

def control_drone(tello, key):
 # Define the drone control commands based on keyboard inputs
    if key == 'w':
        tello.send_rc_control(0, 20, 0, 0)  # Move forward
    elif key == 's':
        tello.send_rc_control(0, -20, 0, 0)  # Move backward
    elif key == 'a':
        tello.send_rc_control(-20, 0, 0, 0)  # Move left
    elif key == 'd':
        tello.send_rc_control(20, 0, 0, 0)   # Move right
    if key == 'i':
        tello.send_rc_control(0, 0, 20, 0)  # Move up
    elif key == 'k':
        tello.send_rc_control(0, 0, -20, 0)  # Move down
    elif key == 'h':
        tello.send_rc_control(0, 0, 0, 0) #hover
    elif key == 'l':
        tello.send_rc_control(0, 0, 0, 20)  # Turn clockwise
    elif key == 'j':
        tello.send_rc_control(0, 0, 0, -20)  # Turn counterclockwise
    elif key == 'q':
        tello.land()  # Land
        
def main():
    tello = Tello()  # Create a Tello object
    tello.connect()  # Connect to the Tello drone
    tello.streamon()  # Start the video stream
    tello.takeoff()  # Take off

    # Initialize face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Add hotkeys to control the drone
    keyboard.add_hotkey('w', lambda: control_drone(tello, 'w'))
    keyboard.add_hotkey('s', lambda: control_drone(tello, 's'))
    keyboard.add_hotkey('a', lambda: control_drone(tello, 'a'))
    keyboard.add_hotkey('d', lambda: control_drone(tello, 'd'))
    keyboard.add_hotkey('i', lambda: control_drone(tello, 'i'))
    keyboard.add_hotkey('k', lambda: control_drone(tello, 'k'))
    keyboard.add_hotkey('j', lambda: control_drone(tello, 'j'))
    keyboard.add_hotkey('l', lambda: control_drone(tello, 'l'))
    keyboard.add_hotkey('h', lambda: control_drone(tello, 'h'))
    keyboard.add_hotkey('q', tello.land)

    run_drone = True  # Flag to control the main loop

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

    while run_drone:
        # Accept a new incoming connection
        client_socket, client_address = server_socket.accept()
        
        print(f"Accepted connection from {client_address}")

        # Start a new thread to handle the client
        client_handler = ClientHandler(client_socket, tello)
        client_handler.start()

        try:
            frame = tello.get_frame_read().frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                if w * h < 4000:  # Change the size threshold as needed
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red color for smaller faces
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color for other faces

                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

            cv2.imshow('Tello Face Detection', frame)

            # Check for keyboard input
            if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('a') or keyboard.is_pressed('d') or keyboard.is_pressed('q'):
                key = keyboard.read_event().name
                control_drone(tello, key)
            elif keyboard.is_pressed('esc'):
                run_drone = False
            
        except KeyboardInterrupt:
            tello.land()
            run_drone = False
        
    tello.land()
    cv2.destroyAllWindows()
    tello.streamoff()
    tello.end()

if __name__ == "__main__":
    main()