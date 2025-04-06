import cv2 #import open CV
import serial #for arduino communication
import time  #for the time delay

crossHairLength = 100
goalThreshold = 50
deadzone = 20

serialBus = serial.Serial("COM3",9600)

def main():
    imageCapture = cv2.VideoCapture(1) #link var to camera 

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #load Cascade that is faces

    if not imageCapture.isOpened: #failure to open cam
        print("failed to open Camera")
        exit()

    while True:
        validCapture, frame = imageCapture.read() #frame is the image and the width and height of the image, and specifies it is colored
        #frame = cv2.transpose(frame)
        #frame = cv2.flip(frame, flipCode=-1)

        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]



        grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #convert image to grey scale

        faces = face_cascade.detectMultiScale(grayFrame, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30)) #using grayscale photo
        #minSize in min pixel size of a detection
        # scale factor is the the size that the detection window increases over every iteration. Starts at min size and increases by factor.
        #scaleFactor allows to detect objects of different sizes or depths. Too large is better computationally but may not detect as well
        #min neighbors is the number of detection windows that must also read a face beside eachother to confirm a detection
        #high min neighbors means stricter detection, low means more false positives but better for crowds, and partially covered faces


        if validCapture:  

            
            #draw on frame, point1(top left), point2(bottom right), color(BGR), thickness(pixels)   
            
            if len(faces)!=0:
                largestArea = 0
                faceIndex = 0
                for i in range(len(faces)):
                    area = faces[i][2] * faces[i][3]
                    if area > largestArea:
                        faceIndex = i

                x,y,w,h = faces[faceIndex]

                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle over face 

                dX,dY = getDiffCoord(x + (w/2),y+(h/2),frameWidth,frameHeight)
                cv2.putText(frame,f"dX{dX}, dY{dY}",(int(frameWidth*0.6),int(frameHeight*0.6)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
                goalAcheived = abs(dX) < goalThreshold and abs(dY) <goalThreshold
                sendCommands(dX,dY)
            else:
                goalAcheived = False
                sendCommands(0,0)
            
            if goalAcheived:
                crossHairColor = (0,0,255)
            else:
                crossHairColor= (255,0,0)
            
            #draw cross hair
            cv2.line(frame,(int(frameWidth/2 - crossHairLength/2),int(frameHeight*0.5)),
                     (int(frameWidth/2+crossHairLength/2),int(frameHeight*0.5)) , crossHairColor,2)
            cv2.line(frame,(int(frameWidth*0.5),int(frameHeight/2 - crossHairLength/2)),
                     (int(frameWidth*0.5),int(frameHeight/2 + crossHairLength/2)),crossHairColor,2)
            cv2.circle(frame,(int(frameWidth/2),int(frameHeight/2)),goalThreshold,(0,255,0),2)   
            #line: frame, point 1, point2, color (BRG), thickness(pixels)
            
            
            cv2.imshow("captured image",frame) #create window of Frame


            if cv2.waitKey(1) ==27: #wait 1 ms while detecting for a click of any key
                print("exiting")
                break                
           
        else:
            print("Failed to capture image")
            break


    imageCapture.release() #release the camera from being used by openCV
    cv2.destroyAllWindows() #destroy the windows

def getDiffCoord(x,y,w,h):
    dx = int(x - (w/2))
    dy = int(y- (h/2))
    return dx,dy

def sendCommands(dx,dy):
    #if abs(dy) < deadzone:
    #    dy = 0
    #if abs(dx) < deadzone:
    #    dx = 0
    serialBus.write(f'{dx} {dy}\n'.encode('utf-8'))





if __name__ == '__main__':
    main()