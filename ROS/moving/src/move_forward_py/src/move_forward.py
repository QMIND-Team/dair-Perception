import rospy
# from std_msgs.msg import Movement
from geometry_msgs.msg import *
import math
rospy.init_node('image_listener', anonymous=True)
def MovementCallback(msg):
    vel_msg = Twist()
    # if(msg.x >= 0):
    #     if(msg.x > 320):
    #         vel_msg.linear.x = 0
    #         vel_msg.linear.y = 0
    #         vel_msg.linear.z = 0
    #         vel_msg.angular.z = -0.5
    #         vel_msg.angular.y = 0
    #         vel_msg.angular.x = 0
    #     else:
    #         vel_msg.linear.x = 0
    #         vel_msg.linear.y = 0
    #         vel_msg.linear.z = 0
    #         vel_msg.angular.z = 0.5
    #         vel_msg.angular.y = 0
    #         vel_msg.angular.x = 0


    # Angular velocity proportional control
    target = 320
    gain = 0.0005*2
    if (msg.x >= 0):
        error = (target-msg.x)
        vel_msg.angular.z = gain*error
    else:
        vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
rospy.Subscriber("/Object_Locations", Point32, MovementCallback)
rospy.spin()