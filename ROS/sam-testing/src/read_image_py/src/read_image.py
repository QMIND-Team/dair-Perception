#!/usr/bin/env python

# Goal of this program is to read images from the robot and try to process them
import sys, time
import numpy as np 
from scipy.ndimage import filters

import roslib
import rospy
# Image message
from sensor_msgs.msg import CompressedImage
# OpenCV2 image converter
# from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 used to save image
import cv2

#Instantiate CvBridge
# bridge = CvBridge()

VERBOSE = False

font = cv2.FONT_HERSHEY_SIMPLEX

def image_callback(msg):
    print("Received an image!")
    if VERBOSE:
        print 'received image of type: "%s"' % msg.format

    # convert to cv2
    np_arr = np.fromstring(msg.data, np.uint8)
    # image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Trying face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    #draw rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(image_np, "Face", (x,y), font, 1, (255,0,0),1)
        if (x > 340):
            cv2.putText(image_np, "Left", (x,y+35), font, 1, (255,0,0),1)
        else:
            cv2.putText(image_np, "Right", (x,y+35), font, 1, (255,0,0),1)

    cv2.imshow('cv_img', image_np)
    cv2.waitKey(0)
    cv2.imwrite('./photos/test.jpg', image_np)


def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/raspicam_node/image/compressed"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, CompressedImage, image_callback)
    #rospy.Publisher("/output/image_raw/compressed", CompressedImage)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
