import time
import numpy as np
import cv2
import sys
sys.path.append(".")

def Main():
    fn = sys.argv[1]
    fn2 = fn.split("_")
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
            cc = '%4d' % count
            imgname = "../img/" + fn2[0] + "/img" + cc + ".jpg"
            imwrite(imgname,ff)

if name == "__main__":
    Main()
