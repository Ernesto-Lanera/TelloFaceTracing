from djitellopy import tello
import cv2

# Create a window and set its name
cv2.namedWindow("Drone")

# Initialize Tello
drone = tello.Tello()

# Connect to the drone
drone.connect()

# Start the video stream
drone.streamon()

# Loop until the user closes the window

while True:
    # Read frame from video stream
    frame = drone.get_frame_read().frame
    
    # Swap R and B channels
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Show the frame in the created window
    cv2.imshow("Drone", frame_rgb)

    # Wait for the user to press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Close the window and end the video stream
cv2.destroyAllWindows()
drone.streamoff()

# Disconnect from the drone
drone.end()