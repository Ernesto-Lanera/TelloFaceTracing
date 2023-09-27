from ultis import *


width,height = 320 , 240
pid = [0,5,0,5,0]
pError = 0 
startCounter = 0 

myDrone = initializeTello()



while True:

    ##Flight
    if startCounter == 0:
         myDrone.takeoff()

    
    ## step 1  
    Img = telloGetFrame(myDrone,width,height)
    ## step 2
    img, info = findFace(img)
    ##step 3
    pError = trackFace(myDrone,info,width,pid,pError) 
    print(info[0][0]) 
    cv2.imshow('image',Img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         myDrone.land()
         break
                   