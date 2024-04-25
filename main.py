import cv2
import time
import math
import numpy as np
import handtracking as ht
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cam = cv2.VideoCapture(0)
ptime = 0

detector = ht.handDetector(detectionCon=1,maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volper = 0
volBar = 400

while True:
    ret, img = cam.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) !=0:
        x1 , y1 = lmlist[4][1], lmlist[4][2]
        x2 , y2 = lmlist[8][1], lmlist[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2
        
        cv2.circle(img,(x1,y1),10,(255,51,51),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,51,51),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,51,51),5)
        cv2.circle(img,(cx,cy),10,(255,51,51),cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        vol = np.interp(length, [30,150],[-65,0])
        volBar = np.interp(length, [30,150],[400,150])
        volper = np.interp(length, [30,200],[0,100])
        volume.SetMasterVolumeLevel(vol, None)

        # print(vol)
        if length<30:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
    
    img = cv2.flip(img,1)
    cv2.rectangle(img,(50,int(volBar)),(80,400),(0,0,255),cv2.FILLED)
    cv2.putText(img,f"{int(volper)}%",(50,400),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    
    
    cv2.putText(img,f"FPS: {int(fps)}",(40,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),3)
    cv2.imshow('Image',img)
    if cv2.waitKey(1) == 27:
        exit()