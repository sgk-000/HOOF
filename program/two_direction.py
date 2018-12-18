import sys
import time
import skvideo.io
sys.path.append(".")

import cv2
import numpy as np

fn = sys.argv[1]
print(fn)
cap = cv2.VideoCapture(fn)

if not cap.isOpened():
	print ("could not open: ")
	sys.exit()

caplen = int(cap.get(7))
fps = int(cap.get(5))
print ("Video length: ",caplen)
print("Frame per Second: ", fps)
#sys.exit()
w_num = int(sys.argv[2])
h_num = int(sys.argv[3])
prev = None
curr = None
count = 1
ee = np.zeros((caplen,h_num*w_num))

count = int(cap.get(1))
ret, frame = cap.read()
print (count, ret)
#frame = cv2.resize(frame,None,fx=0.5,fy=0.5)
height, width = frame.shape[:2]
celh = int(height/h_num)
celw = int(width/w_num)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
prev = gray

#out = skvideo.io.FFmpegWriter("output.mp4")

while(True):
	count = int(cap.get(1))
	ret, frame = cap.read()
	print (count, ret)
	if ret is False:
		break
#	frame = cv2.resize(frame,None,fx=0.5,fy=0.5)
	height, width = frame.shape[:2]
	celh = int(height/h_num)
	celw = int(width/w_num)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	e2 = np.zeros((h_num,w_num))
	curr = gray
	edge = cv2.Canny(curr, 300, 300)
	flow = cv2.calcOpticalFlowFarneback(prev,curr,None,0.5,3,15,3,5,1.2,0)
	mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])
        ret,th = cv2.threshold(mag,1,255,cv2.THRESH_BINARY)
	for j in range (0,h_num):
		for i in range(0,w_num):
                        hh = th[(j-1)*celh:j*celh-1, (i-1)*celw:i*celw-1]
			e2[j,i] = np.sum(hh)/255.0
	prev = curr
	ee[count,:] = np.ravel(e2)
        for i in range(1,h_num):
                cv2.line(th,(0,celh*i),(width,celh*i),(0,0,255),2)
                for j in range(1,w_num):
                        cv2.line(th,(celw*j,0),(celw*j,height),(0,0,255),2)
	cv2.imshow('th',th)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#np.savetxt(fn+".csv",dd,delimiter=",")
#out.close()
cap.release()
cv2.destroyAllWindows()
