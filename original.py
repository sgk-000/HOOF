import sys
import time
sys.path.append(".")

import cv2
import numpy as np

for i in range(3):
    for j in range(4):
        i = 2
        if i == 0:dir = "60fps(横)"
        if i == 1:dir = "120fps(横)"
        if i == 2:dir = "240fps(横)"
        if j == 0:fil = "120rpm.MP4"
        if j == 1:fil = "240rpm.MP4"
        if j == 2:fil = "360rpm.MP4"
        if j == 3:fil = "480rpm.MP4"
        fn = str(dir) + '/' + str(fil)
        if i == 2: fn = "240fps(横)" + fil
        #print(fn)
        cap = cv2.VideoCapture(fn)

        if not cap.isOpened():
            print ("could not open: ",fn)
            sys.exit()

        caplen = int(cap.get(7))
        print ("Video length: ", caplen)
        prev = None
        curr = None
        count = 1
        count = int(cap.get(1))
        ret, ff = cap.read()
        print (count, ret)
        frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        while(True):
            count = int(cap.get(1))
            ret, ff = cap.read()
            print (count, ret)
            if ret is False:
                break
            frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
            height, width = frame.shape[:2]

            cv2.imshow('bgr',frame)
            if i == 0: dir2 = "original_60fps_"
            if i == 1: dir2 = "original_120fps_"
            if i == 2: dir2 = "original_240fps_"
            if j == 0: fil2 = "120rpm.png"
            if j == 1: fil2 = "240rpm.png"
            if j == 2: fil2 = "360rpm.png"
            if j == 3: fil2 = "480rpm.png"
            if count == 1499: cv2.imwrite(str(dir2)+'_'+str(fil2)+'_1499',frame)
            if count == 1500: cv2.imwrite(str(dir2)+'_'+str(fil2)+'_1500',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
