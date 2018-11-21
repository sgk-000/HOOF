import sys
import time
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
w_num = sys.argv[2]
h_num = sys.argv[3]
prev = None
curr = None
count = 1
dd = np.zeros((caplen,h_num*w_num*8))

count = int(cap.get(1))
ret, ff = cap.read()
print (count, ret)
frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
height, width = frame.shape[:2]
celh = int(height/h_num)
celw = int(width/w_num)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame)
hsv[:,:,1] = 255
bgr = frame
d8 = np.zeros((h_num,w_num,8))
d16 = np.zeros((h_num,w_num,16))
prev = gray

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('./output.avi', fourcc, 30.0, (height,width))


while(True):
	count = int(cap.get(1))
	ret, ff = cap.read()
	print (count, ret)
	if ret is False:
		break
	frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
	height, width = frame.shape[:2]
        celh = int(height/h_num)
	celw = int(width/w_num)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame)
	hsv[:,:,1] = 255
	bgr = frame
	d8 = np.zeros((h_num,w_num,8))
	d16 = np.zeros((h_num,w_num,16))
	curr = gray
	edge = cv2.Canny(curr, 300, 300)
	flow = cv2.calcOpticalFlowFarneback(prev,curr,None,0.5,3,15,3,5,1.2,0)
	mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])
	hsv[:,:,0] = ang*180/np.pi/2
	hsv[:,:,2] = cv2.min(mag*30,255)
	a2 = np.floor((ang)*15.9999995/(2*np.pi))
	#print(np.max(a2),np.min(a2))
	for j in range (0,h_num):
		for i in range(0,w_num):
			for k in range(0,16):
				aa = a2[(j-1)*celh:j*celh-1, (i-1)*celw:i*celw-1]
				mm = mag[(j-1)*celh:j*celh-1, (i-1)*celw:i*celw-1]
				d16[j,i,k] = np.sum(mm[np.where(aa==k)])
			d8[j,i,0] = d16[j,i,0] + d16[j,i,15]
			for k in range(1,8):
				d8[j,i,k] = np.sum(d16[j,i,2*k-1:2*k])
	g = hsv[:,:,2]
	hsv[:,:,2] = cv2.max(g,edge)
	hsv[:,:,1] = 255-edge;
	bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
	prev = curr

	dd[count,:] = np.ravel(d8)
        for i in range(1,h_num):
                cv2.line(bgr,(0,celh*i),(width,celh*i),(0,0,255),2)
                for j in range(1,w_num):
                        cv2.line(bgr,(celw*j,0),(celw*j,height),(0,0,255),2)
	cv2.imshow('bgr',bgr)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#np.savetxt(fn+".csv",dd,delimiter=",")
out.release()
cap.release()
cv2.destroyAllWindows()
