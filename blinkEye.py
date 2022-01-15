import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture('video11.mp4')
# detect faces in the video and max 1 face 
detector = FaceMeshDetector(maxFaces=1) 
plotY = LivePlot(640, 360, [20, 50], invert=True)
# positions for the left eye 
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]

ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

while True:
    # to make the frame on (replayin video)

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    # find face in the video 
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            #draw circle in the face and it is filled ==> you can not see that 
            cv2.circle(img, face[id], 5,color, cv2.FILLED)

        leftUp = face[159]   # top of the left eye 
        leftDown = face[23]   # down of the left eye 
        leftLeft = face[130]   # left part of the left eye 
        leftRight = face[243]   # right part of the left eye 
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)   # distance between leftup and leftdown 
        #print(lenghtVer)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)   # distance between left part and right part
        #print(lenghtHor)
        print(int((lenghtVer/lenghtHor)*100))

        #draw a line between top and down to clairify the distance between them 
        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        #draw a line between top and down to clairify the distance between them 
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0,200,0)
            counter = 1
        #else :

            #print("ratioAvg , counter",ratioAvg , counter)
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255,0, 255)

        cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (100, 100)  , 
                           colorR=color  , font=cv2.FONT_HERSHEY_PLAIN)

        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)

    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", imgStack)
    cv2.waitKey(25)