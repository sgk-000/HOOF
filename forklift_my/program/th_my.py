import sys
import time
import os
sys.path.append(".")

import cv2
import numpy as np


for c in range(0,3):
	if c == 0:
		celw = 3
		celh = 3
	if c == 1:
		celw = 5
		celh = 5
	if c == 2:
		celw = 7
		celh = 7

	for a in range(0,3):
		for e in range(1,16):
			if a == 0:
				alpha = "A"
			if a == 1:
				alpha = "B"
			if a == 2:
				alpha = "C"

			fn = "../E2/e_data/" + alpha + "/" + str(e) + "_e2.avi"
			print(fn)
			dir = "../E2/" + alpha + "_res/" + str(celw) + "_" + str(celh) +"/"
			cap = cv2.VideoCapture(fn)
			cap2 = cv2.VideoCapture(fn)

			if not cap.isOpened():
				print ("could not open: ")
				sys.exit()

			fn, dl = os.path.splitext(fn)
			caplen = int(cap2.get(7))
			print ("Video length: ")
			prev = None
			curr = None
			count = 1
			#dd = np.zeros((caplen,celh*celw*8))


			count = int(cap.get(1))
			cou = 1
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
			print(alpha,e)
			print (count, ret)
			#frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
			height, width = frame.shape[:2]
			h3 = int(height/celh)
			w3 = int(width/celw)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			hsv = np.zeros_like(frame)
			hsv[:,:,1] = 255
			bgr = frame
			prev = gray

			fourcc = cv2.VideoWriter_fourcc(*'XVID')
			#out = cv2.VideoWriter(dir+"out/"+fn+str(celw)+"_"+str(celh)+"out.avi", fourcc, 30.0, (height,width))


			while(True):
				count = int(cap2.get(1))
				#ret, ff = cap.read()
				ret, frame = cap2.read()
				#print (count, ret)
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
				e8 = np.zeros((celh,celw))
				curr = gray
				edge = cv2.Canny(curr, 300, 300)
				flow = cv2.calcOpticalFlowFarneback(prev,curr,None,0.5,3,15,3,5,1.2,0)
				mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])
				ret,th = cv2.threshold(mag,1,255,cv2.THRESH_BINARY)
				th2 = np.array(th)
				#print(th2)
				hsv[:,:,0] = ang*180/np.pi/2
				hsv[:,:,2] = cv2.min(mag*30,255)
				for j in range (0,celh):
					for i in range(0,celw):
						hh = th[(j)*h3:(j+1)*h3-1, i*w3:(i+1)*w3-1]
						hh2 = np.array(hh)

						e8[j,i] = np.sum(hh)/255.0
						e88 = np.array(e8)

				prev = curr
				ee[count,:] = np.ravel(e8)
				#cv2.imshow('th',th)
				#cv2.imshow('bgr',bgr)
				#cv2.imshow('frame',frame)
				cv2.imwrite("img\\"+fn+str(celw)+"_"+str(count)+"of.png", bgr);
				cv2.imwrite("img\\"+fn+str(celw)+"_"+str(count)+"bw.png", th);
				#try:
					#print("in");
					#out.write(bgr)
				#except:
					#print("no write")
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

			fil = str(e) + "_e_"
			#np.savetxt(dir+str(celw)+"_"+str(celh)+"d.csv",dd,delimiter=",")
			np.savetxt(dir+fil+str(celw)+"_"+str(celh)+"e2.csv",ee[1:count,:],delimiter=",")
			#out.release()
			cap.release()
			cap2.release()
			cv2.destroyAllWindows()
