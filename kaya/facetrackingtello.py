import cv2
from djitellopy import Tello
 

def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0 
    myDrone. left_rightvelocity = 0
    myDrone.up_down_velocity = 0 
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def telloGetFrame(myDrone, w= 320,h=240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img 

width = 320
height = 240 
startCounter =0 

myDrone = initializeTello()

while True:
    ## step 1  
    Img = telloGetFrame(myDrone,width,height)

    cv2.imshow('image',Img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         myDrone.land()
         break
                   