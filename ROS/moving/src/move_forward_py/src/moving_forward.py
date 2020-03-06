#!/usr/bin/env python
import rospy
# from std_msgs.msg import Movement
from geometry_msgs.msg import *
import math
import numpy as np
from sensor_msgs.msg import LaserScan 

class move_bot:

    def __init__(self):
        self.velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        buffer_size = 52428800
        self.subscriber  = rospy.Subscriber("/Object_Locations", Point32, self.MovementCallback, queue_size=1, buff_size=buffer_size)

    def laser_scan(self):
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

    def MovementCallback(self, msg):
        print 'x value: {}'.format(msg.x)
        vel_msg = Twist()
        # Set forward velocity
        ranges_scan = self.laser_scan()
        # Find point of min range
        minDist = 1000 # just needs to be some high number
        for i in range(0,len(ranges_scan)):
            if ranges_scan[i][1] < minDist:
                minDist = ranges_scan[i][1]
                minAngle = ranges_scan[i][0]
        if (msg.x >= 0):
            target = 0.4
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
        self.velocity_publisher.publish(vel_msg)
    

def main(args):
    ic = move_bot()
    rospy.init_node('movement', anonymous=True)
    try:
        rospy.spin()
    except:
        print 'error'

def myhook():
    print "\nTurning off movement..."
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    
    velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    velocity_publisher.publish(vel_msg)

rospy.on_shutdown(myhook)

if __name__ == '__main__':
    main(sys.argv)