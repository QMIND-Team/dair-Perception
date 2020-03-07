import rospy
# from std_msgs.msg import Movement
from geometry_msgs.msg import *
import math
import numpy as np
from sensor_msgs.msg import LaserScan 
rospy.init_node('image_listener', anonymous=True)
def laser_scan():
    ranges_scan=[]
    # msg = rospy.wait_for_message("scan_filtered", LaserScan)
    msg = rospy.wait_for_message("scan", LaserScan)
    rangeMax = 10
    rangeMin = 349
    for i in range(rangeMax,-2,-1) + range(359, rangeMin,-1):
        if   np.nan_to_num(msg.ranges[i] ) != 0 :
                #ranges_scan.append(np.nan_to_num(self.msg.ranges[i]))
                ranges_scan.append([i,np.nan_to_num(msg.ranges[i])])
        elif (i+1) in range(rangeMax,-2,-1) + range(359, rangeMin,-1) and (i-1) in range(rangeMax,-2,-1) + range(359, rangeMin,-1) and np.nan_to_num(msg.ranges[i]) == 0:
                #ranges_scan.append((np.nan_to_num(self.msg.ranges[i+1])+np.nan_to_num(self.msg.ranges[i-1]))/2)
                ranges_scan.append([i,(np.nan_to_num(msg.ranges[i+1])+np.nan_to_num(msg.ranges[i-1]))/2])
        else :
                #ranges_scan.append(np.nan_to_num(self.msg.ranges[i]))
                ranges_scan.append([i,np.nan_to_num(msg.ranges[i])])
    return ranges_scan

def MovementCallback(msg):
    vel_msg = Twist()
    # Set forward velocity
    ranges_scan = laser_scan()
    # Find point of min range
    minDist = 1000 # just needs to be some high number
    for i in range(0,len(ranges_scan)):
        if ranges_scan[i][1] < minDist:
            minDist = ranges_scan[i][1]
            minAngle = ranges_scan[i][0]
    #print("dist = {:.2f}\tang = {:.2f}\n".format(minDist,minAngle))
    # Proportional control
    # target = 0.3
    # error = -1*(target - minDist)
    # if error < 0.0:
    #     error = 0.0
    # elif error > 1.5:
    #     error = 1.5
    # gain = 0.2  
    # vel_msg.linear.x = error*gain
    # if (error == 0):
    #     vel_msg.angular.z = 0
    # # Angular velocity proportional control (sets angular velocity)
    # target = 320
    # gain = 0.001
    # if (msg.x >= 0):
    #     error = (target - msg.x)
    #     vel_msg.angular.z = gain*error
    # else:
    #     vel_msg.angular.z = 0
    if (msg.x >= 0):
        target = 0.3
        error = -1*(target - minDist)
        if error < 0.0:
            error = 0.0
        elif error > 1.5:
            error = 1.5
        linear_gain = 0.1
        vel_msg.linear.x = error*linear_gain
        target = 320
        angular_gain = 0.001
        error = (target - msg.x)
        vel_msg.angular.z = angular_gain*error
    else:
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0.2
    velocity_publisher.publish(vel_msg)
velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
rospy.Subscriber("/Object_Locations", Point32, MovementCallback)
rospy.spin()