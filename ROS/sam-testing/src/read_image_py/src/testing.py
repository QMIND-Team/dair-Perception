#import rospy
import os
import pickle # "Pickling" (i.e. serialization) means to convert an object into a byte stream - "unpickling" means the opposite
#from sensor_msgs.msg import LaserScan # takes a single scan from a planar laser range-finder (http://docs.ros.org/api/sensor_msgs/html/msg/LaserScan.html)
#from geometry_msgs.msg import Twist # used to control motor velocity (http://docs.ros.org/api/geometry_msgs/html/msg/Twist.html)
#import numpy as np
clf = pickle.load(open('clf', "rb"))
#self.clf2 = pickle.load(open(self.config_dir + '/clf2', "rb"))
#self.labels = {'30_0':0, '30_l':1, '30_r':2, '45_0':3, '45_l':4, '45_r':5,'15_0':6, 'empty':7}
#[x for (x , y) in self.labels.iteritems() if y == self.clf2.predict(laser_data_set) ] ## Predict the position
print(type(clf))