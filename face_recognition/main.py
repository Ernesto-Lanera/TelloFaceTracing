import cv2
import os
import socket
import keyboard
from djitellopy import Tello

# Create a TCP/IP socket
sock_dashboard = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
sock_dashboard.bind(server_address)

# Listen for incoming connections
sock_dashboard.listen(1)

# Initialize Tello drone
tello = Tello()
tello.connect()
tello.streamon()

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create a folder to save captured images
if not os.path.exists("captured_images"):
    os.mkdir("captured_images")

# Tello's IP and h
tello_address = ('192.168.10.1', 8889)

# Create a UDP socket for sending commands
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a local port to receive responses
sock.bind(('', 9000))

# Function to send a command to the Tello Drone
def send_command(command):
    try:
        sock.sendto(command.encode('utf-8'), tello_address)
        response, ip = sock.recvfrom(1024)
        return response.decode('utf-8')
    except Exception as e:
        return str(e)

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
        tello.send_rc_control(0, 0, 0, 0)  # Hover
    elif key == 'l':
        tello.send_rc_control(0, 0, 0, 20)  # Turn clockwise
    elif key == 'j':
        tello.send_rc_control(0, 0, 0, -20)  # Turn counterclockwise
    elif key == 'q':
        tello.land()  # Land

def main():
    try:
        # Take off
        tello.takeoff()

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

        # wait for connection
        connection, client_address = sock_dashboard.accept()
            
        while True:
        
            try:
                print('connection from', client_address)

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
                    
                print(frame.shape)
                    
                # wait for labview command
                data = connection.recv(16)

                # Display the frame with face detection
                if data:
                    connection.sendall(frame)
                else:
                    print('no data from', client_address)
                    break
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        tello.land()
    finally:
        # Clean up the connection
        connection.close()
        tello.land()
        tello.streamoff()
        cv2.destroyAllWindows()
        tello.end()

if __name__ == "__main__":
    main()
