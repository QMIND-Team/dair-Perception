
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

# Proportional gain
P_GAIN = 4


class LinearController:
	# constructor
	def __init__(self,p_gain):
		# assign controller parameters
		self.p_gain = p_gain

		# initial conditions
		self.setpoint = 0.

		# set up publisher
		self.velocity_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

		# setup subscribers
		self.setpoint_sub = rospy.Subscriber('setpoint',Float64,self.setpointCallback)
		self.position_sub = rospy.Subscriber('odom',Odometry,self.positionCallback)

		self.timer = rospy.Timer(rospy.Duration(0.1),self.timeoutCallback)

	

	# callback function for incoming setpoint
	def setpointCallback(self,msg):
		self.setpoint = float(msg.data)

	# callback function for incoming robot position
	def positionCallback(self,msg):
		# calculate control input
		position = float(msg.pose.pose.position.x)
		error = self.setpoint - position
		input_ = error * self.p_gain

		# create message
		command = Twist()
		command.linear.x = input_

		# publish velocity
		self.velocity_pub.publish(command)


#
rospy.init_node('linear_controller')
#
controller = LinearController(P_GAIN)

# wait for message
rospy.spin()
