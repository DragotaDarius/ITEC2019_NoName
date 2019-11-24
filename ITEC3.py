
'''
 ("Ball tracking") with OpenCV
    Adapted from the original code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018
'''

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

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

def obj_position(x,y):
    print ("[INFO] oBJECT CENTER COORDONATES AT X0 = {0} AND YO={1}".format(x,y))
def turn_position (x,y,radius):

    if(radius>150):
        d_c=40
        p1a.ChangeDutyCycle(d_c)
        p1b.ChangeDutyCycle(d_c)
        p2a.ChangeDutyCycle(d_c)
        p2b.ChangeDutyCycle(d_c)
        GPIO.output(in1_right,GPIO.LOW)
        GPIO.output(in2_right,GPIO.HIGH)
        GPIO.output(in3_left,GPIO.HIGH)
        GPIO.output(in4_left,GPIO.LOW)

        GPIO.output(in1_left,GPIO.HIGH)
        GPIO.output(in2_left,GPIO.LOW)
        GPIO.output(in3_right,GPIO.LOW)
        GPIO.output(in4_right,GPIO.HIGH)



    elif(radius<50):
        d_c=25
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
    elif(radius<=150 and radius>=50):
        if(x<220):
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
            print("turning left")
        elif(x>420):
            d_c=100
            p1a.ChangeDutyCycle(d_c)
            p1b.ChangeDutyCycle(d_c)
            p2a.ChangeDutyCycle(d_c)
            p2b.ChangeDutyCycle(d_c)
            GPIO.output(in1_right,GPIO.HIGH)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_right,GPIO.HIGH)
            GPIO.output(in4_right,GPIO.LOW)
            #time.sleep(0.01)

            GPIO.output(in1_left,GPIO.HIGH)
            GPIO.output(in2_left,GPIO.LOW)
            GPIO.output(in3_left,GPIO.HIGH)
            GPIO.output(in4_left,GPIO.LOW)
            print("turning right")
        else:
            GPIO.output(in1_right,GPIO.LOW)
            GPIO.output(in2_right,GPIO.LOW)
            GPIO.output(in3_left,GPIO.LOW)
            GPIO.output(in4_left,GPIO.LOW)
            GPIO.output(in1_left,GPIO.LOW)
            GPIO.output(in2_left,GPIO.LOW)
            GPIO.output(in3_right,GPIO.LOW)
            GPIO.output(in4_right,GPIO.LOW)

#frame = imutils.rotate(frame, angle=180)
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (13, 100, 100)
colorUpper = (33, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, inverted ("vertical flip" w/ 180degrees),
	# blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	#frame = imutils.rotate(frame, angle=180)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			turn_position(int(x), int(y), int(radius))
			obj_position(int(x), int(y))
	else:
		GPIO.output(in1_right,GPIO.LOW)
		GPIO.output(in2_right,GPIO.LOW)
		GPIO.output(in3_left,GPIO.LOW)
		GPIO.output(in4_left,GPIO.LOW)

		GPIO.output(in1_left,GPIO.LOW)
		GPIO.output(in2_left,GPIO.LOW)
		GPIO.output(in3_right,GPIO.LOW)
		GPIO.output(in4_right,GPIO.LOW)

	# update the points queue
	pts.appendleft(center)

		# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
