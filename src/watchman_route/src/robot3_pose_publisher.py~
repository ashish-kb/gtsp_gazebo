#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
from geometry_msgs.msg import (
    PoseArray,
    PoseStamped,
    Pose,
    Point,
    Twist,
    TransformStamped,
    Quaternion,
)

if __name__ == '__main__':
    rospy.init_node('robot_pose_publisher')
    p = rospy.Publisher('robot_exploration_pose', Pose)
    listener = tf.TransformListener()
    msg=Pose()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
			(trans,rot) = listener.lookupTransform('/map', '/robot3/base_link', rospy.Time(0))
			msg.position.x=trans[0]
			msg.position.y=trans[1]
			msg.position.z=trans[2]
			msg.orientation.x=rot[0]
			msg.orientation.y=rot[1]
			msg.orientation.z=rot[2]
			msg.orientation.w=rot[3]
			p.publish(msg)                        

            
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        rate.sleep()
