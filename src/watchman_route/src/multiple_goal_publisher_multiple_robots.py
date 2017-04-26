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
import sys
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback, MoveBaseActionResult
import numpy as np
from actionlib_msgs.msg import GoalStatus

list_of_robots=[]
move_base_list=[]
list_of_completion=[]
list_goal_counter=[]
universal_counter=0
def listener(robotsList):
	global list_goal_counter
	global list_of_completion
	global move_base_list
	for robot in robotsList:
		filename=robot
		filename+='_goals.txt'
		with open(filename, 'r') as fin:
			robotIndex=int(robot[5:6])-1
			data = fin.read().splitlines(True)
			if(list_goal_counter[robotIndex]<len(data)):
				line=data[list_goal_counter[robotIndex]]
				values = line.split("\t")
				goal_x=float(values[0])
				goal_y=float(values[1])
				topicName="/"
				topicName+=robot
				topicName+="/move_base"
				move_base = actionlib.SimpleActionClient(topicName, MoveBaseAction)
				rospy.loginfo("Waiting for move_base action server...")
				move_base.wait_for_server(rospy.Duration(60))
				rospy.loginfo("Connected to move base server")
				rospy.loginfo("Starting Exploration")
				goal = MoveBaseGoal()
				goal.target_pose.pose.position.x = (goal_x)
				goal.target_pose.pose.position.y = (goal_y)
				goal.target_pose.pose.orientation.w = 1
				goal.target_pose.header.frame_id = '/map'
				goal.target_pose.header.stamp = rospy.Time.now()
				move_base_list[robotIndex]=(move_base)
				print("got the goal for : ")
				print(robot)
				print(goal)
				rospy.loginfo("Goal Set!")
				move_base.send_goal(goal)
				list_goal_counter[robotIndex]+=1
			else:
				robotIndex=int(robot[5:6])-1
				list_of_completion[robotIndex]=True
				checkCompletion()
	checkStatus()


def checkCompletion():
	if(all(list_of_completion)):
		rospy.loginfo("All goals visited!")
		rospy.loginfo("Exiting!")
		sys.exit()
	rospy.loginfo("Waiting for other robots to reach goals!")


def addToCounter():
	global universal_counter
	universal_counter+=1

def navigationComplete():
	rospy.loginfo("All goals visited!")
	rospy.loginfo("Exiting!")
	sys.exit()

def checkStatus():
	rospy.loginfo("Checking status!")
	global move_base_list
	global list_of_completion 
	counter=1
	print(move_base_list)
	if(move_base_list):
		for move_base in move_base_list:
			goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 'SUCCEEDED', 'ABORTED', 'REJECTED','PREEMPTING', 'RECALLING', 'RECALLED','LOST']
			failed_states=['ABORTED', 'REJECTED','RECALLED','LOST']
			move_base.wait_for_server(rospy.Duration(60))
			robot="robot"
			robot+=str(counter)
			robotIndex=counter-1
			state = move_base.get_state()
			if state == GoalStatus.SUCCEEDED and list_of_completion[robotIndex]==False:
				rospy.loginfo("Goal succeeded!")
				rospy.sleep(1)
				rospy.loginfo("Done!! Move to next goal!")
				robotsList=[]
				print("goal reached by ")
				print(robot)
				rotateInPlace(robot)
				robotsList.append(robot)
				listener(robotsList)
			elif(state in failed_states):
				rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))
				robot=str(move_base)[1:6]
				print("goal failed ")
				print(robot)
				rotateInPlace(robot)
				rospy.loginfo("Goal failed!! Move to next goal!")
				robotsList=[]
				robotsList.append(robot)
				listener(robotsList)
			counter+=1
		rospy.loginfo("Goals Active! let's check again!")
		rospy.sleep(2)
		checkStatus()
	else:
		navigationComplete

def rotateInPlace(robotName):
    print("This is to make the robot rotate in place!")
    top='/'
    top+=robotName
    top+='/cmd_vel'
    print(str(top))
    p = rospy.Publisher(top, Twist)
    twist = Twist()
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0            
    twist.angular.x = 0
    twist.angular.y = 0  
    twist.angular.z = 0.5
    for i in range(60):
        p.publish(twist)
        rospy.sleep(0.1) 

    twist = Twist()
    rospy.loginfo("Stopping!")
    p.publish(twist)
    rospy.sleep(1.)

def create_goal_list(robotsList):
	for robot in robotsList:
		filename=robot
		filename+='_goals.txt'
		with open(filename, 'r') as fin:
			data = fin.read().splitlines(True)
			list_of_goals.append(data)

if __name__ == '__main__':
	global list_of_robots
	global move_base_list
	global list_goal_counter
	global list_of_completion
	print('Initialized')
	no_of_robs=sys.argv[1]
	robotsList=[]
	counter=1
	print("number of ROBOTS")
	#print(no_of_robs)
	while(counter<=int(no_of_robs)):
		rob="robot" + str(counter)
		robotsList.append(rob)
		move_base_list.append(rob)
		list_goal_counter.append(0)
		list_of_completion.append(False)
		print("counter   :  "+str(counter))
		counter+=1
	rospy.init_node('multiple_goal_publisher', anonymous=True)
	list_of_robots=robotsList[:]
	#create_goal_lists(robotsList)
	listener(robotsList)
