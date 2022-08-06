#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:33:19 2021

@author: guoxiong
"""



import rospy
import math
import tf
from geometry_msgs.msg import Twist
from human_robot_transport.msg import Position

D = 1.2 #设置robot1与robot2之间的距离D


if __name__ == "__main__":
    rospy.init_node("follower")
    listener = tf.TransformListener() 
    vel_pub = rospy.Publisher("robot2/cmd_vel", Twist, queue_size=1)
    msg = Twist()
    rate = rospy.Rate(200.0)
    Xintegral = 0
    Xprevious_error = 0
    Yintegral = 0
    Yprevious_error = 0
    Kp = 100
    Ki = 0.2
    Kd = 0.1
    while not rospy.is_shutdown():
        human_position = rospy.wait_for_message("predicted_position", Position)
        angular = math.atan2(human_position.y, human_position.x) 
        distance = math.sqrt(human_position.x ** 2 + human_position.y ** 2)
        Xerror = human_position.x * (distance - D) / distance
        Yerror = human_position.y * (distance - D) / distance
        
        print(Xerror)
        Xintegral = Xintegral + Xerror
        if abs(Xerror) < 0.02:
            Xintegral = 0
        Yintegral = Yintegral + Yerror
        if abs(Yerror) < 0.02:
            Yintegral = 0
        
        Xderivative = Xerror - Xprevious_error
        Yderivative = Yerror -Yprevious_error
        Xprevious_error = Xerror
        Yprevious_error = Yerror
        
        msg.linear.x = Kp * Xerror + Ki * Xintegral + Kd * Xderivative
        msg.linear.y = Kp * Yerror + Ki * Yintegral + Kd * Yderivative
        msg.angular.z = Kp * angular
        
        vel_pub.publish(msg)
#        print(msg.linear.x)
        rate.sleep()

        
