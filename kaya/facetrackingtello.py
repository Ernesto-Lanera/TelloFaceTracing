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

def telloGetFrame(myDrone, w= 360,h=240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    r, g, b = im_rgb.split()
    im_rgb = Image.merge('RGB', (b, g, r))
    myDrone = initializeTello()
    return img 

w,h = 360,240

while True:
    ## step 1
    Img = telloGetFrame(myDrone,w,h)

    cv2.imshow('image',Img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         myDrone.land()
         break
                   