import mediapipe as mp
import cv2
import time
import math

class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

        self.pTime = 0
        self.cTime = 0

        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, frame, draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList

    def getFPS(self, frame):
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        cv2.putText(frame, f"{str(int(fps))} fps", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        return frame
    
    def findDistance(self, p1, p2, frame):
        x1, y1 = p1[1], p1[2]
        x2, y2 = p2[1], p2[2]
        distance = math.hypot(x2 - x1, y2 - y1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(frame, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
        return distance, frame

    def fingersUp(self, lmList):
        fingers = []

        if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers