#!/usr/bin/env python
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
from geometry_msgs.msg import Point32
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
desired_object = ''


class image_read:

    def __init__(self):
        self.item = raw_input('What are you looking for: ')
        '''Initialize ROS publisher and subscriber'''
        #publish topics
        self.image_pub = rospy.Publisher("/Object_Detection/bounded_image/compressed", CompressedImage, queue_size=1)
        self.coords_pub = rospy.Publisher("/Object_Locations", Point32, queue_size=1)
        #subscribed topic
        image_topic = "/raspicam_node/image/compressed"
        buffer_size = 52428800
        self.subscriber = rospy.Subscriber( image_topic, CompressedImage, self.callback, queue_size=1, buff_size=2**24)

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
        # Limit framerate to roughly 5fps to decrease computer load
        # if (speed < 0.20):
        #     time.sleep(0.20-speed)

        start = time.time()

        # Create a new image with the predicted boxes and labels
        found, coord = plot_boxes(image_np, res, class_names, self.item, plot_labels = True)
      
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

        finish = time.time()

        print 'I took {:.3f}'.format(finish-start), 'seconds to finish the remaining processes (boxes, publish)'

        '''
        Publishing coordinates 
        '''
        # variables: found, coord
        found_object_msg = Point32()
        found_object_msg.y = 0
        found_object_msg.z = 0
        if found:
            found_object_msg.x = coord
        else:
            found_object_msg.x = -1
        self.coords_pub.publish(found_object_msg)
        


def main(args):
    try:
        global.desired_object = args
    except NameError:
        global.desired_object = 'clock'
    ic = image_read()
    rospy.init_node('image_listener', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print 'Interrupted'
    sys.exit(0)
        
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
