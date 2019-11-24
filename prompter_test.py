#!/usr/bin/python
from subprocess import Popen, PIPE
from time import time, sleep
from nbstreamreader import NonBlockingStreamReader as NBSR
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

in1_right = 11
in2_right = 13
in3_right = 15
in4_right = 7
enA_right = 33
enB_right = 35

in1_left = 16
in2_left = 18
in3_left = 38
in4_left = 40
enA_left = 32
enB_left = 12
d_c=80

#GPIO.setmode(GPIO.BCM)
GPIO.setup(in1_left,GPIO.OUT)
GPIO.setup(in2_left,GPIO.OUT)
GPIO.setup(in3_left,GPIO.OUT)
GPIO.setup(in4_left,GPIO.OUT)
#right
GPIO.setup(in1_right,GPIO.OUT)
GPIO.setup(in2_right,GPIO.OUT)
GPIO.setup(in3_right,GPIO.OUT)
GPIO.setup(in4_right,GPIO.OUT)

GPIO.setup(enA_left,GPIO.OUT)
GPIO.setup(enB_left,GPIO.OUT)
GPIO.setup(enA_right,GPIO.OUT)
GPIO.setup(enB_right,GPIO.OUT)
#GPIO.setup(29,GPIO.OUT)
#GPIO.setup(31,GPIO.OUT)
GPIO.output(enA_left,GPIO.HIGH)
GPIO.output(enB_left,GPIO.HIGH)
GPIO.output(enA_right,GPIO.HIGH)
GPIO.output(enB_right,GPIO.HIGH)

GPIO.output(in1_left,GPIO.LOW)
GPIO.output(in2_left,GPIO.LOW)
GPIO.output(in3_left,GPIO.LOW)
GPIO.output(in4_left,GPIO.LOW)

GPIO.output(in1_right,GPIO.LOW)
GPIO.output(in2_right,GPIO.LOW)
GPIO.output(in3_right,GPIO.LOW)
GPIO.output(in4_right,GPIO.LOW)

p1a=GPIO.PWM(enA_left,1000)
p1b=GPIO.PWM(enB_left,1000)
p2a=GPIO.PWM(enA_right,1000)
p2b=GPIO.PWM(enB_right,1000)
p1a.start(50)
p1b.start(50)
p2a.start(50)
p2b.start(50)

cmd = "./cmd.sh"
start_time=time()
flag=0
t_max=3
i_max=500
i_neutral=i_max
i_happy=i_max
i_sad=i_max
i_surprise=i_max
i_anger=i_max
neutral = 0
sad = 0
happy = 0
anger = 0
surprise = 0
sad_nr = 0
happy_nr = 0
anger_nr = 0
surprise_nr = 0
neutral_nr = 0


p = Popen(cmd,
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
# wrap p.stdout with a NonBlockingStreamReader object:
nbsr = NBSR(p.stdout)
# issue command:
#p.stdin.write('command\n')
# get the output
while True:
    output = nbsr.readline(60)
    #output = p.stdout.read()
    # 0.1 secs to let the shell output the result
    #sleep(0.1)
    if not output:
        print('[No more data]')
        break
    #print (output)
   # time.sleep(0.1)
    flag=0
    #cuv=7
    
    if (output.find('neutral') != -1 ):
        #print (output)
        #print ('neutral223')
        cuv=7
        s=output.index('neutral')
        neutral=output[s+cuv+3:s+cuv+7]
        neutral_nr=float(neutral)
        #print (neutral)
    if (output.find('happy') != -1 ):
        #print (output)
        #print ('happy1231')
        cuv=5
        s=output.index('happy')
        happy=output[s+cuv+3:s+cuv+7]
        happy_nr=float(happy)
        #print (happy)
    if (output.find('sad') != -1 ):
        #print (output)
        #print ('sad123')
        cuv=3
        s=output.index('sad')
        sad=output[s+cuv+3:s+cuv+7]
        sad_nr=float(sad)
        #print (sad)
    if (output.find('surprise') != -1 ):
        #print (output)
        #print ('surprise234')
        cuv=8
        s=output.index('surprise')
        surprise=output[s+cuv+3:s+cuv+7]
        surprise_nr=float(surprise)
        #print (surprise)
    if (output.find('anger') != -1 ):
        #print (output)
        #print ('anger234')
        cuv=5
        s=output.index('anger')
        anger=output[s+cuv+3:s+cuv+7]
        anger_nr=float(anger)
        #print (anger)
    emotie=max(neutral_nr,happy_nr,sad_nr,surprise_nr,anger_nr)
    
    #print (emotie)
    
    if (emotie == neutral_nr and flag == 0):
        i_neutral=i_neutral-1
        if (i_neutral == 0 and flag == 0):
            flag = 1
            print('stau pe loc')
            i_neutral= i_max
            start_time = time()
            #neutral = 0
    if(emotie == happy_nr and flag == 0):
        
        i_happy=i_happy-1
        if (i_happy == 0 and flag == 0):
            flag = 1
            print('dau din coada')
            i_happy= i_max
            start_time = time()
            d_c=60
            p1a.ChangeDutyCycle(d_c)
            p1b.ChangeDutyCycle(d_c)
            p2a.ChangeDutyCycle(d_c)
            p2b.ChangeDutyCycle(d_c)
            GPIO.output(in1_right,GPIO.HIGH)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_left,GPIO.LOW)
            GPIO.output(in4_left,GPIO.HIGH)
            
            GPIO.output(in1_left,GPIO.LOW)
            GPIO.output(in2_left,GPIO.HIGH)
            GPIO.output(in3_right,GPIO.HIGH)
            GPIO.output(in4_right,GPIO.LOW)
            sleep(0.25)
            GPIO.output(in1_right,GPIO.LOW)
            GPIO.output(in2_right,GPIO.HIGH)
            GPIO.output(in3_left,GPIO.HIGH)
            GPIO.output(in4_left,GPIO.LOW)

            GPIO.output(in1_left,GPIO.HIGH)
            GPIO.output(in2_left,GPIO.LOW)
            GPIO.output(in3_right,GPIO.LOW)
            GPIO.output(in4_right,GPIO.HIGH)
            sleep(0.25)
            GPIO.output(in1_left,GPIO.LOW)
            GPIO.output(in2_left,GPIO.LOW)
            GPIO.output(in3_left,GPIO.LOW)
            GPIO.output(in4_left,GPIO.LOW)

            GPIO.output(in1_right,GPIO.LOW)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_right,GPIO.LOW)
            GPIO.output(in4_right,GPIO.LOW)
            sleep(1.5)
            
    if(emotie == sad_nr and flag == 0):
        
        i_sad=i_sad-1
        if (i_sad == 0 and flag == 0):
            flag = 1
            print('ma apropiu')
            i_sad= i_max
            start_time = time()
            d_c=30
            p1a.ChangeDutyCycle(d_c)
            p1b.ChangeDutyCycle(d_c)
            p2a.ChangeDutyCycle(d_c)
            p2b.ChangeDutyCycle(d_c)
            GPIO.output(in1_right,GPIO.HIGH)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_left,GPIO.LOW)
            GPIO.output(in4_left,GPIO.HIGH)
            GPIO.output(in1_left,GPIO.LOW)
            GPIO.output(in2_left,GPIO.HIGH)
            GPIO.output(in3_right,GPIO.HIGH)
            GPIO.output(in4_right,GPIO.LOW)
            sleep(0.5)
            GPIO.output(in1_left,GPIO.LOW)
            GPIO.output(in2_left,GPIO.LOW)
            GPIO.output(in3_left,GPIO.LOW)
            GPIO.output(in4_left,GPIO.LOW)

            GPIO.output(in1_right,GPIO.LOW)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_right,GPIO.LOW)
            GPIO.output(in4_right,GPIO.LOW)
            sleep(1.5)
            
    if(emotie == surprise_nr and flag == 0):
        
        i_surprise=i_surprise-1
        if (i_surprise == 0 and flag == 0):
            flag = 1
            print('ma misc')
            i_surprise= i_max
            start_time = time()
            d_c=100
            p1a.ChangeDutyCycle(d_c)
            p1b.ChangeDutyCycle(d_c)
            p2a.ChangeDutyCycle(d_c)
            p2b.ChangeDutyCycle(d_c)
            GPIO.output(in1_right,GPIO.LOW)
            GPIO.output(in2_right,GPIO.HIGH)
            GPIO.output(in3_right,GPIO.LOW)
            GPIO.output(in4_right,GPIO.HIGH)
            #time.sleep(0.01)
            GPIO.output(in1_left,GPIO.LOW)
            GPIO.output(in2_left,GPIO.HIGH)
            GPIO.output(in3_left,GPIO.LOW)
            GPIO.output(in4_left,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(in1_right,GPIO.HIGH)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_right,GPIO.HIGH)
            GPIO.output(in4_right,GPIO.LOW)
            #time.sleep(0.01)

            GPIO.output(in1_left,GPIO.HIGH)
            GPIO.output(in2_left,GPIO.LOW)
            GPIO.output(in3_left,GPIO.HIGH)
            GPIO.output(in4_left,GPIO.LOW)
            sleep(0.5)
            GPIO.output(in1_left,GPIO.LOW)
            GPIO.output(in2_left,GPIO.LOW)
            GPIO.output(in3_left,GPIO.LOW)
            GPIO.output(in4_left,GPIO.LOW)

            GPIO.output(in1_right,GPIO.LOW)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_right,GPIO.LOW)
            GPIO.output(in4_right,GPIO.LOW)
            sleep(1)
            
            
            
    if(emotie == anger_nr and flag == 0):
#         print('TASDIME')
        i_anger=i_anger-1
        if (i_anger == 0 and flag == 0):
            flag = 1
            print('fug')
            i_anger= i_max
            start_time = time()
    
    if (time()-start_time >2  and flag == 1):
        i_neutral=i_max
        i_happy=i_max
        i_sad=i_max
        i_surprise=i_max
        i_anger=i_max   
        flag=0
        #print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        GPIO.output(in1_left,GPIO.LOW)
        GPIO.output(in2_left,GPIO.LOW)
        GPIO.output(in3_left,GPIO.LOW)
        GPIO.output(in4_left,GPIO.LOW)

        GPIO.output(in1_right,GPIO.LOW)
        GPIO.output(in2_right,GPIO.LOW)
        GPIO.output(in3_right,GPIO.LOW)
        GPIO.output(in4_right,GPIO.LOW)
