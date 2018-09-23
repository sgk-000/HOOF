import sys
import time
import os
sys.path.append(".")

import cv2
import numpy as np

fn = sys.argv[1]
print(fn)
cap = cv2.VideoCapture(fn)
cap2 = cv2.VideoCapture(fn)
if not cap.isOpened():
	print "could not open: ",fn
	sys.exit()

fn, dl = os.path.splitext(fn)
caplen = int(cap.get(7))
print "Video length: ", caplen
celw = 7
celh = 7
prev = None
curr = None
count = 1
#dd = np.zeros((caplen,celh*celw*8))
cou = 1
count = int(cap.get(1))
while(True):
	count = int(cap.get(1))
	cou = count
	ret, frame = cap.read()
	if ret is False:
		break

print(cou)
ee = np.zeros((cou,celh*celw))


#ret, ff = cap.read()
ret, frame = cap2.read()
print count, ret
#frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
height, width = frame.shape[:2]
h3 = int(height/celh)
w3 = int(width/celw)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame)
hsv[:,:,1] = 255
bgr = frame
prev = gray

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter(fn+str(celw)+"_"+str(celh)+"out.avi", fourcc, 30.0, (height,width))


while(True):
	count = int(cap2.get(1))
	#ret, ff = cap.read()
	ret, frame = cap2.read()
	print count, ret
	if ret is False:
		break
	#frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
	height, width = frame.shape[:2]
	h3 = int(height/celh)
	w3 = int(width/celw)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame)
	hsv[:,:,1] = 255
	bgr = frame
	#d8 = np.zeros((celh,celw,8))
	#d16 = np.zeros((celh,celw,16))
	e8 = np.zeros((celh,celw))
	curr = gray
	edge = cv2.Canny(curr, 300, 300)
	flow = cv2.calcOpticalFlowFarneback(prev,curr,None,0.5,3,15,3,5,1.2,0)
	mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])
	ret,th = cv2.threshold(mag,1,255,cv2.THRESH_BINARY)
	hsv[:,:,0] = ang*180/np.pi/2
	hsv[:,:,2] = cv2.min(mag*30,255)
	a2 = np.floor((ang)*15.9999995/(2*np.pi))
	#print(np.max(a2),np.min(a2))
	for j in range (0,celh):
		for i in range(0,celw):
	#		aa = a2[(j-1)*h3:j*h3-1, (i-1)*w3:i*w3-1]
	#		mm = mag[(j-1)*h3:j*h3-1, (i-1)*w3:i*w3-1]
			hh = th[(j-1)*h3:j*h3-1, (i-1)*w3:i*w3-1]
			e8[j,i] = np.sum(hh)/255.0

	#		for k in range(0,16):
				#print (np.sum(th[np.where(aa==k)]))
		#		d16[j,i,k] = np.sum(mm[np.where(aa==k)])/(np.sum(hh[np.where(aa==k)])/255.0)
			#	if d16[j,i,k] == float("inf"):
			#		d16[j,i,k] = 0
			#d8[j,i,0] = d16[j,i,0] + d16[j,i,15]
			#for k in range(1,8):
			#	d8[j,i,k] = np.sum(d16[j,i,2*k-1:2*k])

	g = hsv[:,:,2]
	hsv[:,:,2] = cv2.max(g,edge)
	hsv[:,:,1] = 255-edge;
	bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
	prev = curr

	#dd[count,:] = np.ravel(d8)
	ee[count,:] = np.ravel(e8)
	#cv2.imshow('th',th)
	#cv2.imshow('bgr',bgr)
	##cv2.imshow('frame',frame)
	#cv2.imwrite("img\\"+fn+str(celw)+"_"+str(count)+"of.png", bgr);
	#cv2.imwrite("img\\"+fn+str(celw)+"_"+str(count)+"bw.png", th);
	#try:
	#	print("in");
	#	out.write(bgr)
	#except:
	#	print("no write")
	#if cv2.waitKey(1) & 0xFF == ord('q'):
	#	break

#np.savetxt(fn+str(celw)+"_"+str(celh)+"d.csv",dd,delimiter=",")
np.savetxt(str(celw)+"_"+str(celh)+"e.csv",ee,delimiter=",")
#out.release()
cap.release()
cap2.release()
cv2.destroyAllWindows()
