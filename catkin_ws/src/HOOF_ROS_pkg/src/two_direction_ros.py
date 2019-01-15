#!/usr/bin/env python
## Author: Koby
# Purpose: Ros node to Histogram of optical flow

import sys
import time
sys.path.append(".")

import cv2
import numpy as np

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class Hoof_node:

        def __init__(self,w_num,h_num):
                self.hoof_pub = rospy.Publisher("hoof_image_two",Image,queue_size=1)
                self.image_sub = rospy.Subscriber("image", Image, self.hoof)
                self.bridge = CvBridge()
                self.w_num = w_num
                self.h_num = h_num
                self.curr_image =None
                self.prev_image = None
                self.ee = np.zeros([])
                self.count = 0


        def hoof(self,image):
                try:
                        cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
                except CvBridgeError as e:
                        print(e)
                self.curr_image=cv2.cvtColor(cv_image,cv2.COLOR_BGR2RGB)
                self.count = self.count + 1
                ff = self.curr_image
                frame = cv2.resize(ff,None,fx=0.5,fy=0.5)
                height, width = frame.shape[:2]
                celh = int(height/self.h_num)
                celw = int(width/self.w_num)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                e2 = np.zeros((self.h_num,self.w_num))
                if(self.count == 1): self.prev_image = gray
                self.curr_image = gray
                edge = cv2.Canny(self.curr_image, 300, 300)
                flow = cv2.calcOpticalFlowFarneback(self.prev_image,self.curr_image,None,0.5,3,15,3,5,1.2,0)
                mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])
                ret,th = cv2.threshold(mag,1,255,cv2.THRESH_BINARY)
                for j in range (0,self.h_num):
                        for i in range(0,self.w_num):
                                hh = th[(j-1)*celh:j*celh-1, (i-1)*celw:i*celw-1]
			        e2[j,i] = np.sum(hh)/255.0

                self.prev_image = self.curr_image
	        self.ee = np.append(self.ee,np.ravel(e2))
                
                for i in range(1,self.h_num):
                        cv2.line(th,(0,celh*i),(width,celh*i),(0,0,255),2)
                        for j in range(1,self.w_num):
                                cv2.line(th,(celw*j,0),(celw*j,height),(0,0,255),2)
                
                th = np.uint8(th)
                img = th.reshape((self.curr_image.shape))
                image_out = Image()
                try:
                        image_out = self.bridge.cv2_to_imgmsg(img,"mono8")
                except CvBridgeError as e:
                        print(e)
                        image_out.header = image.header
                self.hoof_pub.publish(image_out)


def main():
        rospy.init_node("hoof_two")
        args = []
        args.append( rospy.get_param('w_num') )
        args.append( rospy.get_param('h_num') )
        obj = Hoof_node(args[0],args[1])
        try:
                rospy.spin()
        except KeyboardInterrupt:
                print("Shutdown")
        cv2.destroyAllWindows()

if __name__=='__main__':
        main()
