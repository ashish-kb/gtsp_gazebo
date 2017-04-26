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
import sys

def listener(ClickedPoint,filename):
	print("Entered main function")
	file = open(filename, "a")
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
	scan(filename)

def scan(filename):
	print("scanning")
	msg = rospy.wait_for_message("/clicked_point", PointStamped)
	listener(msg,filename)

if __name__ == '__main__':
	no_of_robot=sys.argv[1]
	filename="robot"
	filename+=no_of_robot
	filename+='_goals.txt'
	rospy.init_node('goal_text_creator', anonymous=True)
	open(filename, 'w').close()
	print("Initiated")
	scan(filename)