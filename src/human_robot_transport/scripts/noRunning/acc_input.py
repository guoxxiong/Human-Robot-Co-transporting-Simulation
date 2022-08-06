#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:22:53 2021

@author: guoxiong
"""


import rospy
import tf
from geometry_msgs.msg import Twist


if __name__ == "__main__":
    rospy.init_node("acc_input")
    listener = tf.TransformListener() 
    vel_pub = rospy.Publisher("robot1/cmd_vel", Twist, queue_size=1)
    msg = Twist()
    rate = rospy.Rate(400.0)
    count = 0
    while not rospy.is_shutdown():
        msg.linear.x = 0 + 0.005*count 
        count = count + 1 
        if msg.linear.x == 1.5:
            count = 0
        vel_pub.publish(msg)
        print(msg)
        rate.sleep()



        
