#-*- coding: utf-8 -*-

import time
import serial
import serial.tools.list_ports
import sys
sys.path.append("..\Video\Lib")
sys.path.append("..\PID\Lib")
from ImageTracking import *
import PID
import cv2
import numpy as np

##-- Video tracking setting --##
imgT = ImageTracking()
imgT.setResolution(240, 320)
imgT.info()

#Kpy = 1
#Kiy = 6
Kpy = 1
Kiy = 1
Kdy = 0
pidY = PID.PID(Kpy, Kiy, Kdy)
pidY.setVtarget = imgT.imgH/2
pidY.setWindup(255)

##-- Control system setting --##
cMax = 255
cStep = 1


##-- configure the serial connections (the parameters differs on the device you are connecting to) --##
coms=serial.tools.list_ports.comports()
for a in coms:
     print a
'''
ser = serial.Serial(
     port='COM20',
     baudrate=57600,
     parity=serial.PARITY_ODD,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS
)  
ser.isOpen()
'''

##-- Simulation setting --##
simImg = np.zeros((imgT.imgH, imgT.imgW, 3), dtype = "uint8")
realH = 3.0      # 攝影機視野的實際高度 單位:公尺
pixH = realH/imgT.imgH       # 每1個pixel 的實際高度
qX = imgT.imgW/2
qY = 0
start_time = time.time()
qM = 0.01           # 無人機的實際重量 單位:公斤
F2 = 0.0

deltaX = 0
deltaY = 0
while True:

     deltaY = ((0.098-F2) * (time.time()-start_time)**2)/qM
     print 'deltaY=' + str(deltaY)
     if( qY<imgT.imgH or qY>0 ):
          qY = round(deltaY/pixH)
     print 'qY=' + str(qY)
     
     if( qY>imgT.imgH):
          start_time = time.time()
     elif( qY<0 ):
          start_time = time.time()
          qY = imgT.imgH
     
     
     simImg = np.zeros((imgT.imgH, imgT.imgW, 3), dtype = "uint8")
     cv2.circle(simImg, (int(qX), int(qY)), 10, (0,0,255), -1)
     cv2.namedWindow("Simulation", cv2.WINDOW_NORMAL)
     cv2.resizeWindow("Simulation", imgT.imgW*2, imgT.imgH*2)
     cv2.imshow("Simulation", simImg)

    
     k = cv2.waitKey(1) & 0xFF    # press ESC to exit
     if k == 27:
          break
     elif( k==ord('u') ):
          F2 += 0.001
          print 'F2=' + str(F2)

cv2.destroyAllWindows()
#ser.write(chr(int(0)))
imgT.trackingStop()
#ser.close()
