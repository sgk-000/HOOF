import sys
import time
SIZE = 3
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
celw = SIZE
celh = SIZE
prev = None
curr = None
count = 1
dd = np.zeros((caplen,celh*celw*8))

count = int(cap.get(1))
ret, ff = cap.read()
#ret, frame = cap.read()
print (count, ret)
frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
height, width = frame.shape[:2]
h3 = int(height/celh)
w3 = int(width/celw)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame)
hsv[:,:,1] = 255
bgr = frame
d8 = np.zeros((celh,celw,8))
d16 = np.zeros((celh,celw,16))
prev = gray

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./output.avi', fourcc, 30.0, (height,width))


while(True):
	count = int(cap.get(1))
	ret, ff = cap.read()
	#ret, frame = cap.read()
	print (count, ret)
	if ret is False:
		break
	frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
	height, width = frame.shape[:2]
	h3 = int(height/celh)
	w3 = int(width/celw)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame)
	hsv[:,:,1] = 255
	bgr = frame
	d8 = np.zeros((celh,celw,8))
	d16 = np.zeros((celh,celw,16))
	curr = gray
	edge = cv2.Canny(curr, 300, 300)
	flow = cv2.calcOpticalFlowFarneback(prev,curr,None,0.5,3,15,3,5,1.2,0)
	mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])
	hsv[:,:,0] = ang*180/np.pi/2
	hsv[:,:,2] = cv2.min(mag*30,255)
	a2 = np.floor((ang)*15.9999995/(2*np.pi))
	#print(np.max(a2),np.min(a2))
	for j in range (0,celh):
		for i in range(0,celw):
			for k in range(0,16):
				aa = a2[(j-1)*h3:j*h3-1, (i-1)*w3:i*w3-1]
				mm = mag[(j-1)*h3:j*h3-1, (i-1)*w3:i*w3-1]
				d16[j,i,k] = np.sum(mm[np.where(aa==k)])
			d8[j,i,0] = d16[j,i,0] + d16[j,i,15]
			for k in range(1,8):
				d8[j,i,k] = np.sum(d16[j,i,2*k-1:2*k])
	#print(d16)
	#print(d8)
	g = hsv[:,:,2]
	hsv[:,:,2] = cv2.max(g,edge)
	hsv[:,:,1] = 255-edge;
	bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
	prev = curr

	dd[count,:] = np.ravel(d8)
	#print(dd)
	out.write(bgr)
	#cv2.imshow('bgr',bgr)
	#cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
#np.savetxt(fn+".csv",dd,delimiter=",")
out.release()
cap.release()
cv2.destroyAllWindows()
