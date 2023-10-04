import cv2
from djitellopy import Tello

# Initialize the Tello drone
tello = Tello()

# Connect to the drone
tello.connect()

# Start the video stream
tello.streamon()

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to determine if a face is friendly or enemy based on the number of eyes
def classify_face(eyes):
    if len(eyes) >= 2:
        return "Friendly"
    else:
        return "Enemy"

# Function to control the drone
def control_drone(tello):
    while True:
        try:
            command = input("Enter a command (takeoff/land/quit/w/s/a/d/u/j/l/r): ").strip().lower()
            if command == "takeoff":
                tello.takeoff()
            elif command == "land":
                tello.land()
            elif command == "quit":
                tello.land()
                break
            elif command == "flip":
                tello.flip("f")
            elif command == "w":
                tello.move_forward(50)
            elif command == "s":
                tello.move_back(50)
            elif command == "a":
                tello.move_left(50)
            elif command == "d":
                tello.move_right(50)
            elif command == "u":
                tello.move_up(50)
            elif command == "j":
                tello.move_down(50)
            elif command == "l":
                tello.rotate_clockwise(45)
            elif command == "r":
                tello.rotate_counter_clockwise(45)
            else:
                print("Invalid command. Please enter a valid command.")
        except KeyboardInterrupt:
            tello.land()
            break

# Initialize the video capture
while True:
    # Read a frame from the drone's camera
    frame = tello.get_frame_read().frame

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Classify face as friendly or enemy
        status = classify_face(eyes)

        # Draw a box around the face with the appropriate color
        color = (0, 255, 0) if status == "Friendly" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, status, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Show the frame with status boxes
    cv2.imshow('Face Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the video stream and disconnect from the drone
tello.streamoff()
tello.end()
tello.disconnect()
cv2.destroyAllWindows()
