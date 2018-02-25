import json
import subprocess



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

    print (json.dumps(data))

getAllUsbCam()


