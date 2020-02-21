#!/usr/bin/env python3

# Reads images from the robot and applies objec detection model

import sys, time
import subprocess
import numpy as np 
from scipy.ndimage import filters
import roslib
import rospy
from sensor_msgs.msg import CompressedImage
import cv2
import darknet
from matplotlib import pyplot as plt
from utils import *

VERBOSE = False

font = cv2.FONT_HERSHEY_SIMPLEX


namesfile='data/coco.names'
class_names = load_class_names(namesfile)



def image_callback(msg):
    print('\nReceived an image!')
    if VERBOSE:
        print('received image of type: ') # "%s"' % msg.format

    # convert to cv2
    np_arr = np.fromstring(msg.data, np.uint8)
    # image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.imwrite('photos/output-image.jpg', image_np)

    '''
    Pretrained-YOLO
    '''
    # Run the object detection model
    res, speed = darknet.findObjects('photos/output-image.jpg')

    # Print the time it took to detect objects
    print 'It took {:.3f}'.format(speed), 'seconds to detect the objects in the image.'

    # Create a new image with the predicted boxes and labels
    plot_boxes(image_np, res, class_names, plot_labels = True)


    '''
    Publishsing Compressed Image
    '''
    #Create Compressed Image
    msg = CompressedImage()
    msg.header.stamp = rospy.Time.now()
    msg.format = "jpeg"
    msg.data = np.array('photos/bounded-image.jpg'[1]).tostring()
    # Publish new image
    rospy.Publisher("/bounded_output_compressed", CompressedImage, queue_size=1).publish(msg)


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
