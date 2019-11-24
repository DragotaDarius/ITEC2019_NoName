#!/usr/bin/python
from subprocess import Popen, PIPE
from time import time, sleep
from nbstreamreader import NonBlockingStreamReader as NBSR
import vlc

p_neutral = vlc.MediaPlayer("/home/marius/ceva/bonjovi.mp3")
p_happy = vlc.MediaPlayer("/home/marius/ceva/vivaldi.mp3")
p_sad = vlc.MediaPlayer("/home/marius/ceva/worry.mp3")
p_surprise = vlc.MediaPlayer("/home/marius/ceva/metallica.mp3")
p_anger = vlc.MediaPlayer("/home/marius/ceva/bonjovi2.mp3")
cmd = "./cmd.sh"
start_time=time()
flag=0
t_max=30
i_max=15
i_neutral=i_max
i_happy=i_max
i_sad=i_max
i_surprise=i_max
i_anger=i_max
p = Popen(cmd,
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
# wrap p.stdout with a NonBlockingStreamReader object:
nbsr = NBSR(p.stdout)
# issue command:
#p.stdin.write('command\n')
# get the output
while True:
    output = nbsr.readline(60)
    # 0.1 secs to let the shell output the result
    if not output:
        print '[No more data]'
        break
    print output
    if (output.find('neutral') != -1 and flag == 0):
    	print ('neutral\n')
        i_neutral=i_neutral-1
        #i_happy=i_max
        #i_sad=i_max
        #i_surprise=i_max
        #i_anger=i_max
        if (i_neutral == 0 and flag == 0):
           flag=1
	   i_neutral=i_max
	   print ("NEUTRAL123")	
	   start_time = time()
           #p= vlc.MediaPlayer("/home/marius/ceva/bonjovi.mp3")
	   p_neutral.play()
           
    if (output.find('happy') != -1 and flag == 0):
    	print ('happy\n')
	i_happy=i_happy-1
	#i_neutral=i_max
	#i_sad=i_max
	#i_surprise=i_max
	#i_anger=i_max
	if (i_happy == 0 and flag == 0):
           flag=1
	   i_happy=i_max
	   print ("HAPPY123")
	   start_time = time()
           #p= vlc.MediaPlayer("/home/marius/ceva/vivaldi.mp3")
	   p_happy.play()

    if (output.find('sad') != -1 and flag == 0):
    	print ('sad\n')
	i_sad=i_sad-1
	#i_neutral=i_max
	#i_happy=i_max
	#i_surprise=i_max
	#i_anger=i_max
	if (i_sad == 0 and flag == 0):
           flag=1
	   i_sad=i_max
	   print ("SAD123")
	   start_time = time()
           #p= vlc.MediaPlayer("/home/marius/ceva/worry.mp3")
	   p_sad.play()
    if (output.find('anger') != -1 and flag == 0):
    	print ('anger\n')
	i_anger=i_anger-1
	#i_neutral=i_max
	#i_happy=i_max
	#i_surprise=i_max
	#i_sad=i_max
	if (i_anger == 0 and flag == 0):
           flag=1
	   i_anger=i_max
	   print ("ANGER123")
	   start_time = time()
           #vlc.MediaPlayer("/home/marius/ceva/bonjovi2.mp3")
	   p_anger.play()
    if (output.find('surprise') != -1 and flag == 0):
    	print ('surprise\n')
	i_surprise=i_surprise-1
	#i_neutral=i_max
	#i_happy=i_max
	#i_anger=i_max
	#i_sad=i_max
	if (i_surprise == 0 and flag == 0):
           flag=1
	   i_surprise=i_max
	   print ("SURPRISE123")
	   start_time = time()
           #p= vlc.MediaPlayer("/home/marius/ceva/metallica.mp3")
	   p_surprise.play()
    #output="a"
    if (time()-start_time > t_max and flag == 1):
	p_neutral.stop()
	p_happy.stop()
	p_sad.stop()
	p_anger.stop()
	p_surprise.stop()
	i_neutral=i_max
	i_happy=i_max
	i_sad=i_max
	i_surprise=i_max
	i_anger=i_max	
	flag=0
