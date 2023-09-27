from djitellopy import Tello
import cv2

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

def findFace(img):
    faceCascade = cv2.image.png('image.png')
    imgGray =  cv2.cvtColor(img.cv2.COLOR_BGR@Gray)
    faces = FaceCascade.detectMultiScale("imgGray 1.2,4")
