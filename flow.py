import sys
import time
sys.path.append(".")

import cv2
import numpy as np

for i in range(3):
	for j in range(4):
		print(i,j)
		if i == 0:dir = "60fps_hor"
		if i == 1:dir = "120fps_hor"
		if i == 2:dir = "240fps_hor"
		if j == 0:fil = "120rpm.MP4"
		if j == 1:fil = "240rpm.MP4"
		if j == 2:fil = "360rpm.MP4"
		if j == 3:fil = "480rpm.MP4"
		fn = str(dir) + '/' + str(fil)
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
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter('./output.avi', fourcc, 30.0, (height,width))

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
			#print(np.max(a2),np.min(a2))
			#print(d16)
			#print(d8)
			g = hsv[:,:,2]
			hsv[:,:,2] = cv2.max(g,edge)
			hsv[:,:,1] = 255-edge;
			bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
			prev = curr

			#print(dd)
			out.write(bgr)
			cv2.imshow('bgr',bgr)
			if i == 0: dir2 = "flow_60fps_"
			if i == 1: dir2 = "flow_120fps_"
			if i == 2: dir2 = "flow_240fps_"
			if j == 0: fil2 = "120rpm.png"
			if j == 1: fil2 = "240rpm.png"
			if j == 2: fil2 = "360rpm.png"
			if j == 3: fil2 = "480rpm.png"
			if count == 1500:
				cv2.imwrite(str(dir2)+'_'+str(fil2)+'_1500',bgr)
				break
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		out.release()
		cap.release()
		cv2.destroyAllWindows()
