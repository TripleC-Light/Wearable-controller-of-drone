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
Kpx = 1
Kix = 6
Kdx = 0.0001
pidX = PID.PID(Kpx, Kix, Kdx)
pidX.setVtarget = imgT.imgW/2

Kpy = 2.5
Kiy = 1
Kdy = 3.0
pidY = PID.PID(Kpy, Kiy, Kdy)
pidY.setVtarget = imgT.imgH/2
pidY.setWindup(255)
#pidY.setWindup(350)

##-- Control system setting --##
cMax = 255
cStep = 1


##-- configure the serial connections (the parameters differs on the device you are connecting to) --##
coms=serial.tools.list_ports.comports()
for a in coms:
     print a

ser = serial.Serial(
     port='COM20',
     baudrate=57600,
     parity=serial.PARITY_ODD,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS
)  
ser.isOpen()

deltaX = 0
deltaY = 0
while True:
     
     current_time = time.time()
    
     #imgT.trackingStart()
     imgT.trackingTurbo()
    
     '''
     deltaX = imgT.X - imgT.imgW/2
     print deltaX, deltaY
     '''

     '''
     if( imgT.X==-1 ):
          deltaX = 0
     else:
          pidX.update(255-imgT.X)
          deltaX = pidX.output
          deltaX += 256
          deltaX /= 2
          if( deltaX>cMax ):
               deltaX = cMax
          if( deltaX<0 ):
               deltaX = 0
          deltaX = round((deltaX/cStep))*cStep
     '''
    
     if( imgT.Y==-1 ):
          deltaY = 0
     else:
          pidY.update(imgT.imgH-imgT.Y)
          deltaY = pidY.output
          deltaY += 256
          deltaY /= 2
          if( deltaY>cMax ):
               deltaY = cMax
          if( deltaY<0 ):
               deltaY = 0
          deltaY = round((deltaY/cStep))*cStep
   
     #ser.write('deltaX=' + str(round(deltaX)) + ', deltaY=' + str(round(deltaY)) + '\r\n')
     ser.write(chr(int(deltaY)))
     fps = 1/(time.time()+0.00001-current_time)
     print 'deltaX=' + str(round(deltaX)) + ', deltaY=' + str(round(deltaY)) + ', FPS=' + str(round(fps)) + ', Time=' + str(round((time.time()-current_time)*1000)) + 'ms'
     #print 'imgT.X=' + str(imgT.X) + ', imgT.Y=' + str(imgT.Y)
    
     k = cv2.waitKey(5) & 0xFF    # press ESC to exit
     if k == 27:
          break
     
     elif( k==ord('s') ):
          setOK = False
          while( setOK==False ):
               Kpy = raw_input('输入Kp：')
               if( Kpy.isdigit() ):
                    Kpy = float(Kpy)
                    pidY.setKp(Kpy)
                    print 'Kp 已經設定為: ' + str(Kpy)
                    setOK = True
               else:
                    print '請輸入數字！'


ser.write(chr(int(0)))
imgT.trackingStop()
ser.close()
