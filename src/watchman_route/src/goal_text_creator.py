#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time
from nav_msgs.msg import Odometry
import math
from geometry_msgs.msg import (
    PoseArray,
    PoseStamped,
    PointStamped,
    Pose,
    Point,
    Twist,
    TransformStamped,
    Quaternion,
)
import numpy as np

def listener(ClickedPoint):
	print("Entered main function")
	file = open("goals.txt", "a")
	goal_x=ClickedPoint.point.x # 
	goal_y=ClickedPoint.point.y # 

	goal_line=str(goal_x)
	goal_line+="\t"
	goal_line+=str(goal_y)
	goal_line+="\n"

	file.write(goal_line)

	print("added the following goal to the line")
	print(goal_line)
	file.close()
	#get the next point
	scan()

def scan():
	print("scanning")
	msg = rospy.wait_for_message("/clicked_point", PointStamped)
	listener(msg)

if __name__ == '__main__':
	rospy.init_node('goal_text_creator', anonymous=True)
	open("goals.txt", 'w').close()
	print("Initiated")
	scan()
