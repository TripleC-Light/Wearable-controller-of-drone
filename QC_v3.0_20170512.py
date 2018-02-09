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
imgT = ImageTracking(0)
imgT.setResolution(120, 160)
imgT.info()

##-- PID control setting --##
Kpx = 2.5
Kix = 0.8
Kdx = 3.5
pidX = PID.PID(Kpx, Kix, Kdx)
pidX.setVtarget = imgT.imgW/2
pidX.setWindup(255)

Kpy = 2.0
Kiy = 0.25
Kdy = 1.5
pidY = PID.PID(Kpy, Kiy, Kdy)
pidY.setVtarget = imgT.imgH/2
pidY.setWindup(255)
#pidY.setWindup(350)

##-- Control system setting --##
startFlag = 0
cMax = 255
cStep = 4


##-- configure the serial connections (the parameters differs on the device you are connecting to) --##

coms=serial.tools.list_ports.comports()
for a in coms:
     print a

ser = serial.Serial(
     port='COM26',
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

          
     if( startFlag==1 ):
          if( imgT.X==-1 ):
               deltaX = 128
          else:
               pidX.update(imgT.imgW-imgT.X)
               deltaX = pidX.output
               deltaX += 256
               deltaX = int(deltaX / 2)
               if( deltaX>cMax ):
                    deltaX = cMax
               if( deltaX<=1 ):
                    deltaX = 1
               deltaX = round((deltaX/cStep))*cStep
          
         
          if( imgT.Y==-1 ):
               deltaY = 1
          else:
               
               pidY.update(imgT.imgH-imgT.Y)
               deltaY = pidY.output
               deltaY += 256
               deltaY = int(deltaY / 2)
               if( deltaY>cMax ):
                    deltaY = cMax
               if( deltaY<=100 ):
                    deltaY = 100
               deltaY = round((deltaY/cStep))*cStep
        
          #ser.write('deltaX=' + str(round(deltaX)) + ', deltaY=' + str(round(deltaY)) + '\r\n')
               
     
          
          ser.write('c')
          ser.write(chr(int(deltaY)))
          #ser.write(chr(int(deltaX)))
          ser.write(chr(int(127)))
          ser.write('0')
          
          fps = 1/(time.time()+0.00001-current_time)
          print 'Kpy=' + str(Kpy) + ', Kiy=' + str(Kiy) + ', Kdy=' + str(Kdy)
          #print 'deltaX=' + str((deltaX*4)+1000) + ', deltaY=' + str((deltaY*4)+1000) + ', FPS=' + str(round(fps)) + ', Time=' + str(round((time.time()-current_time)*1000)) + 'ms'
          #print 'imgT.X=' + str(imgT.X) + ', imgT.Y=' + str(imgT.Y)
     else:
          ser.write('c')
          ser.write(chr(int(0)))
          ser.write(chr(int(127)))
          
          ser.write('0')
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
     elif( k==ord('-') ):
          ser.write('-')
          print ' Press \'-\' '
          
     elif( k==ord('+') ):
          ser.write('+')
          if( startFlag==1 ):
               startFlag = 0
               print ' Control Stop'
          print ' Press \'+\' '

     elif( k==ord('*') ):
          if( startFlag==0 ):
               startFlag = 1
               print ' Press \'*\' , Start Control'
          else:
               startFlag = 0
               print ' Press \'*\' , Control Stop'
               
     elif( k==ord('u') ):
          '''
          Kpy += 0.1
          pidY.setKp(Kpy)
          print ' Kpy=' + str(Kpy)
          '''
          Kiy += 0.05
          pidY.setKi(Kiy)
          print ' Kiy=' + str(Kiy)
          '''
          Kdy += 0.1
          pidY.setKd(Kdy)
          print ' Kdy=' + str(Kdy)
          '''
     elif( k==ord('d') ):
          
          '''
          Kpy -= 0.1
          pidY.setKp(Kpy)
          print ' Kpy=' + str(Kpy)
          '''
          Kiy -= 0.05
          pidY.setKi(Kiy)
          print ' Kiy=' + str(Kiy)
          
          '''
          Kdy -= 0.1
          pidY.setKd(Kdy)
          print ' Kdy=' + str(Kdy)
          '''
         
#ser.write(chr(int(0)))
imgT.trackingStop()
#ser.close()
