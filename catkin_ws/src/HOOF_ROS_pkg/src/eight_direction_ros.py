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
                self.hoof_pub = rospy.Publisher("hoof_image",Image,queue_size=1)
                self.image_sub = rospy.Subscriber("image", Image, self.hoof)
                self.bridge = CvBridge()
                self.w_num = w_num
                self.h_num = h_num
                self.curr_image =None
                self.prev_image = None
                self.dd = np.zeros([])
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
                hsv = np.zeros_like(frame)
                hsv[:,:,1] = 255
                bgr = frame
                d8 = np.zeros((self.h_num,self.w_num,8))
                d16 = np.zeros((self.h_num,self.w_num,16))
                if(self.count == 1): self.prev_image = gray
                self.curr_image = gray

                edge = cv2.Canny(self.curr_image, 300, 300)
                flow = cv2.calcOpticalFlowFarneback(self.prev_image,self.curr_image,None,0.5,3,15,3,5,1.2,0)
                mag, ang = cv2.cartToPolar(flow[...,0],flow[...,1])
                hsv[:,:,0] = ang*180/np.pi/2
                hsv[:,:,2] = cv2.min(mag*30,255)
                a2 = np.floor((ang)*15.9999995/(2*np.pi))
                for j in range (0,self.h_num):
                        for i in range(0,self.w_num):
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
                self.prev_image = self.curr_image
                self.dd = np.append(self.dd,np.ravel(d8))

                for i in range(1,self.h_num):
                        cv2.line(bgr,(0,celh*i),(width,celh*i),(0,0,255),2)
                        for j in range(1,self.w_num):
                                cv2.line(bgr,(celw*j,0),(celw*j,height),(0,0,255),2)

                img=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
                image_out = Image()
                try:
                        image_out = self.bridge.cv2_to_imgmsg(img,"bgr8")
                except CvBridgeError as e:
                        print(e)
                image_out.header = image.header
                self.hoof_pub.publish(image_out)


def main():
        rospy.init_node("hoof_eight")
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
