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
prev = None
curr = None
count = 1
count = int(cap.get(1))
ret, ff = cap.read()
print (count, ret)
frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
height, width = frame.shape[:2]
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame)
hsv[:,:,1] = 255
bgr = frame
prev = gray

#fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'S')
#out = cv2.VideoWriter('./output.mp4', fourcc, 30.0, (height,width))


while(True):
	count = int(cap.get(1))
	ret, ff = cap.read()
	print (count, ret)
	if ret is False:
		break
	frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
	height, width = frame.shape[:2]
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame)
	hsv[:,:,1] = 255
	bgr = frame
	curr = gray
	edge = cv2.Canny(curr, 300, 300)
	flow = cv2.calcOpticalFlowFarneback(prev,curr,None,0.5,3,15,3,5,1.2,0)
	mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])

	hsv[:,:,0] = ang*180/np.pi/2
	hsv[:,:,2] = cv2.min(mag*30,255)
	a2 = np.floor((ang)*15.9999995/(2*np.pi))

	g = hsv[:,:,2]
	hsv[:,:,2] = cv2.max(g,edge)
	hsv[:,:,1] = 255-edge;
	bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
	prev = curr

	#cv2.imshow('bgr',bgr)
	count = '%04d' % count
	write_name = './image' + str(count) + '.png'
	cv2.imwrite(write_name,bgr)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
out.release()
cap.release()
cv2.destroyAllWindows()
