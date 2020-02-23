#!/usr/bin/env python3
'''
Reads images from the robot and applies object detection model
'''
# Import relevant libraries
import sys, time
import subprocess
import numpy as np 
from scipy.ndimage import filters
from scipy import misc
from sensor_msgs.msg import CompressedImage
import cv2
import matplotlib.pyplot as plt
from PIL import Image

# ROS libraries
import roslib
import rospy

# Import local files
import darknet
from utils import *

# Variables
VERBOSE = False 
namesfile='data/coco.names'
class_names = load_class_names(namesfile)


class image_read:

    def __init__(self):
        '''Initialize ROS publisher and subscriber'''
        #publish topic
        self.image_pub = rospy.Publisher("/Object_Detection/bounded_image/compressed", CompressedImage, queue_size=1)
        #subscribed topic
        image_topic = "/raspicam_node/image/compressed"
        self.subscriber = rospy.Subscriber(image_topic, CompressedImage, self.callback, queue_size=1)

    def callback(self, msg):
        print('\nReceived an image!')
        if VERBOSE:
            print 'received image of type: "%s"' % msg.format

        # convert to cv2
        np_arr = np.fromstring(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        cv2.imwrite('photos/output-image.jpg', image_np)

        '''
        Pretrained-YOLO
        '''
        # Run the object detection model
        res, speed = darknet.findObjects('photos/output-image.jpg')

        # Print the time it took to detect objects
        print 'It took {:.3f}'.format(speed), 'seconds to detect the objects in the image.'
        # Limit framerate to roughly 2fps to decrease computer load
        if (speed < 0.5):
            time.sleep(0.5-speed)

        # Create a new image with the predicted boxes and labels
        plot_boxes(image_np, res, class_names, plot_labels = True)
      
        # Read the image with boxes
        box_arr = misc.imread('photos/bounded-image.png')


        '''
        Publishsing Compressed Image
        '''
        #Create Compressed Image
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', box_arr)[1]).tostring()
        # Publish new image
        self.image_pub.publish(msg)


def main(args):
    ic = image_read()
    rospy.init_node('image_listener', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS read_image model"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
