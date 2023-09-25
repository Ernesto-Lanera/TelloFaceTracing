from ultis import *
import cv2


myDrone = initializeTello()

while True:
    ## step 1
    Img = telloGetFrame(myDrone,w,h)

    cv2.imshow('image',Img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         myDrone.land()
         break
                   