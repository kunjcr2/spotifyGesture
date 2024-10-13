# ONLY WORKS ON SPOTIFY DESKPTOP !!!!!!!

import cv2
import numpy as np
from pynput.mouse import Button, Controller as MouseController
import handDetector as hd
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

width = 540
height = 720

cap = cv2.VideoCapture(0)
detector = hd.HandDetector(detectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0

mc = MouseController()
cap.set(3, width)
cap.set(4, height)

allowClick = False
count = 1

while True:
    ret, frame = cap.read()
    detector.findHands(frame)

    lmList = detector.findPosition(frame)

    if len(lmList) != 0:
        fingers = detector.fingersUp(lmList)
        if fingers[4] == 0:
            if fingers == [0, 0, 0, 0, 0]:
                mc.position = (638,550)
                allowClick = True
                count = 1
            elif allowClick and count == 1:
                if fingers==[0,1,0,0,0]:
                    mc.position = (590, 690)
                    mc.click(Button.left, 1)
                    allowClick = False
                    count = 0
                elif fingers==[0,1,1,1,0]:
                    mc.position = (685, 690)
                    mc.click(Button.left, 1)
                    allowClick = False
                    count = 0
                elif fingers == [0, 1, 1, 0, 0]:
                    mc.position = (638, 690)
                    mc.click(Button.left, 1)
                    allowClick = False
                    count = 0
        else:
            allowClick = False
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1+x2)//2, (y1+y2)//2

            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (x1,y1),  (x2,y2), (255, 0, 0), 2)

            length = math.hypot(x2-x1,y2-y1)

            vol = np.interp(length,[50,120],[minVol, maxVol])
            volBar = np.interp(length,[50,120],[300,75])
            volume.SetMasterVolumeLevel(vol, None)

            if length<20:
                cv2.circle(frame, (cx, cy), 8, (0, 255, 0),  cv2.FILLED)


    frame = detector.getFPS(frame)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
