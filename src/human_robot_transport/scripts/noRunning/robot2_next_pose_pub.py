#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 16:32:07 2021

@author: guoxiong
"""


#!/usr/bin/env python
#coding=utf-8
"""
Created on Wed Apr 14 22:58:08 2021

@author: guoxiong
"""


import rospy
import math
import tf
import time
from human_robot_transport.msg import NextPose
from parameters import D

if __name__ == "__main__":
    rospy.init_node("robot2_next_pose_pub")
    listener = tf.TransformListener() 
    pub = rospy.Publisher("robot2/next_pose", NextPose, queue_size = 1)
    rate = rospy.Rate(100.0)

    while not rospy.is_shutdown():
        
        try:
            
            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time())
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        
        angular = math.atan2(trans[1], trans[0])
        distance = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        Xr = trans[0] * (distance - D) / distance
        Yr = trans[1] * (distance - D) / distance
        
        next_pose = NextPose()
        next_pose.x = Xr
        next_pose.y = Yr
        next_pose.theta = angular
        
        pub.publish(next_pose)
        t1 = time.time()
        rate.sleep()
        t2 = time.time()
        print(t2-t1)

        
