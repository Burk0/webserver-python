import json
import subprocess
import cv2
from io import BytesIO
import os


def getAllUsbCam():
    # print(os.system("for I in /sys/class/video4linux/*; do cat $I/index $I/name; done").__class__)
    # list.append(os.system("ls -l /home/buranskyd/"))

    proc = subprocess.Popen(["for I in /sys/class/video4linux/*; do cat $I/index $I/name; done"], stdout=subprocess.PIPE, shell=True)
    # proc = subprocess.Popen(["ls -l "],
    #                         stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    tmp=str(out)[2:len(str(out))-1].split('\\n')
    data = []
    data.append({'desc':tmp[0],'name':tmp[1]})

    # print (json.dumps(data))
    return json.dumps(data)


def getTestCam(id):
    cap = cv2.VideoCapture(int(id))
    if cap.isOpened() is True:
        ret,frame = cap.read()
        if ret == True:
            cv2.imwrite("tmp.jpg",frame)
            file = open("tmp.jpg" ,'rb')
            os.remove("tmp.jpg")
            return file



