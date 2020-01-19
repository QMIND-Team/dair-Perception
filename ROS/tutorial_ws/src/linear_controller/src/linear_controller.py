#!/usr/bin/env python

import rospy

from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

##############
# Parameters #
##############
P_GAIN = 4

class LinearController:
	# Constructor
	def __init__(self, p_gain):

		# Assign controller parameters
		self.p_gain = p_gain
		
		# Set intial Conditions
		self.setpoint = 0
	
		# Setup publisher
		self.velocity_pub = rospy.Publisher('cmd_vel',Twist, queue_size = 10)

		# Setup subscriber
		self.setpoint_sub = rospy.Subscriber('setpoint',Float64, self.setpointCallback)
		self.position_sub = rospy.Subscriber('odom', Odometry, self.positionCallback)

	# Callback function for incoming setpoint
	def setpointCallback(self, msg):
		self.setpoint  = float(msg.data)

	# Callback function for incoming robot position
	def positionCallback(self, msg):
		# Calculate control input
		position = float(msg.pose.pose.position.x)
		error = self.setpoint - position
		input_ = error*self.p_gain

		# Create message
		command = Twist()
		command.linear.x = input_

		# Publish message
		self.velocity_pub.publish(command)



# Main Function #


def main():
	# Initialize Node
	rospy.init_node('linear_controller')

	# Create Controller
	controller = LinearController(P_GAIN)

	# Wait for messages on topic, go to callback function when new messages arrive
	rospy.spin()

# Entry Point #
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
