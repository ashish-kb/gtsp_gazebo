#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time
from nav_msgs.msg import Odometry
import math
from geometry_msgs.msg import (
    PoseArray,
    PoseStamped,
    Pose,
    Point,
    Twist,
    TransformStamped,
    Quaternion,
)


start_time=int(math.floor(time.time()))
prev_time=(int(math.floor(time.time())))
total_distance=0.000
import numpy as np
def listener():
	global start_time
	global prev_time
	global total_distance
	pub = rospy.Publisher('ExplorationDistance', String)
	rospy.init_node('distance_and_time_publisher')
	top="robot_exploration_pose"
	prev_pose = rospy.wait_for_message(top, Pose)
	while(True):
		curr_time=int(math.floor(time.time()))
		while(curr_time==prev_time):
			rospy.sleep(0.1)
			curr_time=int(math.floor(time.time()))
		
		pose = rospy.wait_for_message(top, Pose)

		posex = pose.position.x
		posey = pose.position.y
		curr=np.array((posex,posey))

		prev_posex = prev_pose.position.x
		prev_posey = prev_pose.position.y
		prev=np.array((prev_posex,prev_posey))
		dist_curr=round(np.linalg.norm(curr-prev),2)
		prev_pose=pose
		prev_time = curr_time
		time_elapsed= curr_time- start_time
		print("Time elapsed       :  %s  seconds " % (time_elapsed))
		total_distance = total_distance+dist_curr
		print("Distance traveled  :  %s  meters" % total_distance)
		msg = '\n'
		msg += 'Distance traveled  :  '
		msg += str(total_distance)
		msg += '  meters'
		msg += '\n'
		msg += 'Time elapsed       :  '
		msg += str(time_elapsed)
		msg += '  seconds'
		pub.publish(msg)

if __name__ == '__main__':
	listener()
