# SOURCE:
# https://github.com/ROBOTIS-GIT/turtlebot3_applications
# https://github.com/ROBOTIS-GIT/turtlebot3_applications/blob/master/turtlebot3_follower/nodes/follower
#!/usr/bin/env python
#################################################################################
# Copyright 2018 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#################################################################################
import rospy
from sensor_msgs.msg import LaserScan # takes a single scan from a planar laser range-finder (http://docs.ros.org/api/sensor_msgs/html/msg/LaserScan.html)
from geometry_msgs.msg import Twist # used to control motor velocity (http://docs.ros.org/api/geometry_msgs/html/msg/Twist.html)
import numpy as np
class follower:
    def __init__(self):
        rospy.loginfo('Follower node initialized') 
        # I think this just effectively prints a message, but prints to rosout rather than the command line for easier viewing later (can later view with rqt_console)
        # replaces all occurences of the substrin "nodes" with "config" in self.config_dir
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        # Allows you to publish messages to a topic - you can later publish messages to the topic using the publish() function
        rospy.loginfo('Tree initialized')
        self.follow() # this seems to be the main function, essentially. creating an instance of the class also runs the main function
    def laser_scan(self):
        ranges_scan=[]
        self.msg = rospy.wait_for_message("scan", LaserScan)
        rangeMax = 10
        rangeMin = 349
        for i in range(rangeMax,-2,-1) + range(359, rangeMin,-1):
            if   np.nan_to_num( self.msg.ranges[i] ) != 0 :
                 #ranges_scan.append(np.nan_to_num(self.msg.ranges[i]))
                 ranges_scan.append([i,np.nan_to_num(self.msg.ranges[i])])
            elif (i+1) in range(rangeMax,-2,-1) + range(359, rangeMin,-1) and (i-1) in range(rangeMax,-2,-1) + range(359, rangeMin,-1) and np.nan_to_num(self.msg.ranges[i]) == 0:
                 #ranges_scan.append((np.nan_to_num(self.msg.ranges[i+1])+np.nan_to_num(self.msg.ranges[i-1]))/2)
                 ranges_scan.append([i,(np.nan_to_num(self.msg.ranges[i+1])+np.nan_to_num(self.msg.ranges[i-1]))/2])
            else :
                 #ranges_scan.append(np.nan_to_num(self.msg.ranges[i]))
                 ranges_scan.append([i,np.nan_to_num(self.msg.ranges[i])])
        return ranges_scan

    def follow(self):
        while not rospy.is_shutdown(): # Just checks to see whether the program should shutdown, presumably
            ranges_scan = self.laser_scan()
            twist = Twist()
            # Find point of min range
            minDist = 1000 # just needs to be some high number
            for i in range(0,len(ranges_scan)):
                if ranges_scan[i][1] < minDist:
                    minDist = ranges_scan[i][1]
                    minAngle = ranges_scan[i][0]
            

            # Set forward velocity
            target = 0.3
            error = -1*(target - minDist)
            if error < 0.0:
                error = 0.0
            elif error > 0.5:
                error = 0.5
            gain = 0.3
            twist.linear.x = error*gain
            self.pub.publish(twist)
            print("dist = {:.2f}\tang = {:.2f} \t speed = {:.2f}\n".format(minDist,minAngle, error*gain))
            
            # ## Do something according to each position##
            # if  x == ['30_0']:
            #     twist.linear.x  = 0.13;       twist.angular.z = 0.0;
            # elif x== ['30_l']:
            #     twist.linear.x  = 0.10;       twist.angular.z = 0.4;
            # elif x== ['30_r']:
            #     twist.linear.x  = 0.10;       twist.angular.z = -0.4;
            # elif x== ['45_0']:
            #     twist.linear.x  = 0.13;       twist.angular.z = 0.0;
            # elif x== ['45_l']:
            #     twist.linear.x  = 0.10;       twist.angular.z = 0.3;
            # elif x== ['45_r']:
            #     twist.linear.x  = 0.10;       twist.angular.z = -0.3;
            # elif x== ['15_0']:
            #     twist.linear.x  = 0.0;            twist.angular.z = 0.0;
            # elif x== ['empty']:
            #     twist.linear.x  = 0.0;            twist.angular.z = 0.0;
            # else:
            #     twist.linear.x  = 0.0;            twist.angular.z = 0.0;
            # self.pub.publish(twist)
def main():
    rospy.init_node('follower', anonymous=True)
    try:
        follow = follower()
    except rospy.ROSInterruptException:
        pass    #print("Shutting down")
if __name__ == '__main__':
    main()