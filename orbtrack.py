import sys
import time
sys.path.append(".")

import cv2
import numpy as np


cap = cv2.VideoCapture('./1_collapse.mp4')
#fourcc = cv2.cv.CV_FOURCC(*'XVID')
#out1 = cv2.VideoWriter('output1.avi',fourcc, 19.0, (1280,720))
#out2 = cv2.VideoWriter('output2.avi',fourcc, 19.0, (1280,720))
#out3 = cv2.VideoWriter('output3.avi',fourcc, 19.0, (1280,720))

prev = None
curr = None
count = 1
while(True):
	ret, frame = cap.read()
	print ret, frame
	# Calculate 2 Frame OpticalFlow
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame)
	hsv[:,:,1] = 255
	bgr = frame
	dst2 = frame
	if prev is None:
		prev = gray
	else:
		curr = gray;
		# Optical Flow
		flow = cv2.calcOpticalFlowFarneback(prev,curr,0.5, 3, 15, 3, 5, 1.2, cv2.OPTFLOW_FARNEBACK_GAUSSIAN,None)
		edge = cv2.Canny(curr, 300, 300)
		# Change to Magnitude and Angle
		mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
			
		hsv[:,:,0] = ang*180/np.pi/2
		hsv[:,:,2] = cv2.min(mag*30,255)
		g = hsv[:,:,2]
		hsv[:,:,2] = cv2.max(g,edge)
		hsv[:,:,1] = 255-edge;
		
		#hsv[:,:,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
		bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
		prev = curr
	
	orb = cv2.ORB()
	kp = orb.detect(frame,None)
	kp, des = orb.compute(frame, kp)
	res = cv2.drawKeypoints(bgr,kp,color=(0,255,0), flags=0)
	
	#dst = cv2.pyrMeanShiftFiltering (frame, 20.0, 20.0)
	dst = frame;
	sift = cv2.SIFT()
	kp = sift.detect(gray,None)
	img=cv2.drawKeypoints(dst,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
	hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.2}
	human, r = hog.detectMultiScale(frame, **hogParams)
	for (x, y, w, h) in human:
		cv2.rectangle(img, (x, y),(x+w, y+h),(0,50,255), 3)
	
	dst2 = cv2.pyrMeanShiftFiltering(bgr,30.0,30.0)
	print(count)
	cnt_pad = '%04d' % count
	cv2.imwrite("1/img"+cnt_pad+".png", img)
	cv2.imwrite("1/res"+cnt_pad+".png", res)
	cv2.imwrite("1/dst"+cnt_pad+".png", dst2)
#	out1.write(img)
#	out2.write(res)
#	out3.write(dst2)
	cv2.imshow('frame',img)
	cv2.imshow('bgr',res)
	cv2.imshow('dst2',dst2)
	count = count + 1
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
#out1.release()
#out2.release()
#out3.release()
cv2.destroyAllWindows()	