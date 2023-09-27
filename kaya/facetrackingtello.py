from ultis import *
 
myDrone = initializeTello()

width,height = 320 , 240
while True:
    
    ## step 1  
    Img = telloGetFrame(myDrone,width,height)
    ## step 2
    img = findFace

    cv2.imshow('image',Img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         myDrone.land()
         break
                   