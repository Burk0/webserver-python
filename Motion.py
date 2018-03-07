import cv2
from datetime import datetime
import time

def diffImg(t0,t1,t2):
    d1 = cv2.absdiff(t2,t1)
    d2 = cv2.absdiff(t1,t0)
    return cv2.bitwise_and(d1,d2)

threshold = 81500
# threshold = 150000
cam = cv2.VideoCapture(0)

intervalSpravenieSnimky=10

# winName = "Movement Indicator"
# cv2.namedWindow(winName)

t_minus = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

# cv2.imshow("t_minus", t_minus)
# cv2.imshow("t", t)
# cv2.imshow("t_plus", t_plus)

lastCall = 0

while True:
    cv2.imshow("motion",cam.read()[1])

    if cv2.countNonZero(diffImg(t_minus,t,t_plus)) > threshold and lastCall+intervalSpravenieSnimky<=time.time():
        dimg = cam.read()[1]

        print(time.strftime("%H:%M:%S", time.gmtime(time.time())))
        # cv2.imwrite(datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg',dimg)

        lastCall = time.time()
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)

    key = cv2.waitKey(10)
    if key == 27:
    #     cv2.destroyWindow(winName)
        break

