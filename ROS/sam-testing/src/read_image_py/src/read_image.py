#!/usr/bin/env python3

# Goal of this program is to read images from the robot and try to process them
import sys, time
import subprocess
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

MODEL = "yolov3.weights"
CFG = "yolov3.cfg"

#Instantiate CvBridge
# bridge = CvBridge()

from matplotlib import pyplot as plt
from utils import *
from darknet import Darknet

VERBOSE = False

font = cv2.FONT_HERSHEY_SIMPLEX

# YOLO setup
cfg_file='cfg/yolov3.cfg'
weight_file='weights/yolov3.weights'
namesfile='coco.names'

m = Darknet(cfg_file)
m.load_weights(weight_file)
class_names = load_class_names(namesfile)

# Set the NMS threshold
nms_thresh = 0.6  

# Set the IOU threshold
iou_thresh = 0.4



def image_callback(msg):
    print("Received an image!")
    if VERBOSE:
        print('received image of type: ') # "%s"' % msg.format

    # convert to cv2
    np_arr = np.fromstring(msg.data, np.uint8)
    # image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    '''
    Trying face detection
    '''
    # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # #draw rectangles
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(image_np, (x,y), (x+w, y+h), (255,0,0), 2)
    #     cv2.putText(image_np, "Face", (x,y), font, 1, (255,0,0),1)
    #     if (x > 340):
    #         cv2.putText(image_np, "Left", (x,y+35), font, 1, (255,0,0),1)
    #     else:
    #         cv2.putText(image_np, "Right", (x,y+35), font, 1, (255,0,0),1)

    '''
    Trying pre-trained yolo (instantiation above)
    '''

    # Set the default figure size
    plt.rcParams['figure.figsize'] = [24.0, 14.0]

    # Load the image
    img = image_np

    # Convert the image to RGB
    original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # We resize the image to the input width and height of the first layer of the network.    
    resized_image = cv2.resize(original_image, (m.width, m.height))

    # Detect objects in the image
    boxes = detect_objects(m, resized_image, iou_thresh, nms_thresh)


    '''
    Displaying the final image
    '''
    # Print the objects found and the confidence level
    print_objects(boxes, class_names)

    #Plot the image with bounding boxes and corresponding object class labels
    plot_boxes(original_image, boxes, class_names, plot_labels = True)


    # cv2.imshow('cv_img', img)
    # cv2.waitKey(0)
    # cv2.imwrite('./photos/test.jpg', img)


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
