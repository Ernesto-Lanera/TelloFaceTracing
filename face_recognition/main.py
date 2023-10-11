from djitellopy import Tello
import cv2
import keyboard
import time

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
    try:
        # Create a Tello object
        tello = Tello()

        # Connect to the Tello drone
        tello.connect()

        # Start the video stream
        tello.streamon()

        # Take off
        tello.takeoff()

        # Initialize face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Add hotkeys to control the drone
        keyboard.add_hotkey('w', lambda: control_drone(tello, 'w'))  # Move forward
        keyboard.add_hotkey('s', lambda: control_drone(tello, 's'))  # Move backward
        keyboard.add_hotkey('a', lambda: control_drone(tello, 'a'))  # Move left
        keyboard.add_hotkey('d', lambda: control_drone(tello, 'd'))  # Move right
        keyboard.add_hotkey('i', lambda: control_drone(tello, 'i'))  # Move up
        keyboard.add_hotkey('k', lambda: control_drone(tello, 'k'))  # Move down
        keyboard.add_hotkey('j', lambda: control_drone(tello, 'j'))  # Turn counterclockwise
        keyboard.add_hotkey('l', lambda: control_drone(tello, 'l'))  # Turn clockwise
        keyboard.add_hotkey('h', lambda: control_drone(tello, 'h'))  # hover
        keyboard.add_hotkey('q', tello.land)  # Land

        while True:
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

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        tello.land()
    finally:
        tello.land()
        tello.streamoff()
        cv2.destroyAllWindows()
        tello.end()

if __name__ == "__main__":
    main()
