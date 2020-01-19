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

def image_callback(msg):
    print("Received an image!")
    if VERBOSE:
        print 'received image of type: "%s"' % msg.format

    # convert to cv2
    np_arr = np.fromstring(msg.data, np.uint8)
    # image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    cv2.imshow('cv_img', image_np)
    cv2.waitKey(0)
    cv2.imwrite('./photos/test.jpg', image_np)

def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/raspicam_node/image/compressed"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, CompressedImage, image_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
