import sys
import time
sys.path.append(".")

import cv2
import numpy as np

fn = sys.argv[1]
print(fn)
cap = cv2.VideoCapture(fn)

if not cap.isOpened():
	print ("could not open: ",fn)
	sys.exit()

caplen = int(cap.get(7))
print ("Video length: ", caplen)

count = 1
count = int(cap.get(1))
ret, ff = cap.read()
print (count, ret)
frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
height, width = frame.shape[:2]


fourcc = cv2.VideoWriter_fourcc(*'XVID')



while(True):
    count = int(cap.get(1))
    ret, ff = cap.read()
    print (count, ret)
    if ret is False:
        break
    frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
    height, width = frame.shape[:2]
    cv2.imshow('bgr',frame)
    if count == 1499: cv2.imwrite("original_240fps_480rpm_1499.png",frame)
    if count == 1500: cv2.imwrite("original_240fps_480rpm_1500.png",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
