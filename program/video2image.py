import time
import numpy as np
import cv2
import sys
sys.path.append(".")

def Main():
    for a in range(0,3):
        if a == 0:
            alpha = "A"
        if a == 1:
            alpha = "B"
        if a == 2:
            alpha = "C"

        for i in range(1,16):
            fn = "../E2/e_data/" + alpha + "/" + str(i) + "_e2.avi"
            #fn2 = fn.split("_")
            #print(fn2[0])
            print(fn)
            cap = cv2.VideoCapture(fn)
            if not cap.isOpened():
                print "could not open: ",fn
                sys.exit()

            caplen = int(cap.get(7))
            print "video length+ ", caplen

            while(True):
                count = int(cap.get(1))
                ret,ff = cap.read()

                print count,ret
                if ret is False:
                    break
                imgname = "../E2/e_data/" + alpha + "/" + str(i) + "_img/" + "img" + str(count) + ".jpg"
                cv2.imwrite(imgname,ff)

if __name__ == "__main__":
    Main()
