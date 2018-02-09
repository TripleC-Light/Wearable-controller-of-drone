#-*- coding: utf-8 -*-

import time
import serial
import serial.tools.list_ports
import sys
sys.path.append("..\Video\Lib")
sys.path.append("..\PID\Lib")
from ImageTracking import *
import PID

##-- Video tracking setting --##
imgT = ImageTracking()
imgT.setResolution(240, 320)
imgT.info()

##-- PID control setting --##
Kp = 1
Ki = 6
Kd = 0.0001
pidX = PID.PID(Kp, Ki, Kd)
pidY = PID.PID(Kp, Ki, Kd)
pidX.setVtarget = imgT.imgW/2
pidY.setVtarget = imgT.imgH/2

##-- Control system setting --##
cMax = 255
cStep = 5


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

while True:
     
    current_time = time.time()
    
    #imgT.trackingStart()
    imgT.trackingTurbo()
    
    '''
    deltaX = imgT.X - imgT.imgW/2
    deltaY = imgT.Y - imgT.imgH/2    
    print deltaX, deltaY
    '''
    
    if( imgT.X==-1 ):
         deltaX = 0
    else:
         pidX.update(imgT.X)
         deltaX = pidX.output
         deltaX += 256
         deltaX /= 2
         if( deltaX>cMax ):
              deltaX = cMax
         if( deltaX<0 ):
              deltaX = 0
         deltaX = 255 - deltaX
         deltaX = round((deltaX/cStep))*cStep

    
    if( imgT.Y==-1 ):
         deltaY = 0
    else:
         pidY.update(imgT.Y)
         deltaY = pidY.output
         deltaY += 256
         deltaY /= 2
         if( deltaY>cMax ):
              deltaY = cMax
         if( deltaY<0 ):
              deltaY = 0
         deltaY = 255 - deltaY
         deltaY = round((deltaY/cStep))*cStep
   
    #ser.write('deltaX=' + str(round(deltaX)) + ', deltaY=' + str(round(deltaY)) + '\r\n')
    #ser.write(chr(int(deltaY)))
    fps = 1/(time.time()+0.00001-current_time)
    print 'deltaX=' + str(round(deltaX)) + ', deltaY=' + str(round(deltaY)) + ', FPS=' + str(round(fps)) + ', Time=' + str(round((time.time()-current_time)*1000)) + 'ms'
    #print 'imgT.X=' + str(imgT.X) + ', imgT.Y=' + str(imgT.Y)

    k = cv2.waitKey(5) & 0xFF    # press ESC to exit
    if k == 27:
        break
    
#ser.write(chr(int(0)))
imgT.trackingStop()
#ser.close()

