#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 17:32:08 2021

@author: guoxiong
"""


import rospy
import tf
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from human_robot_transport.msg import Motion
from human_robot_transport.msg import Distance
from human_robot_transport.msg import NextPose
from parameters import D
from parameters import C1_WEIGHT
from parameters import C2_WEIGHT
from parameters import C3_WEIGHT
import time



if __name__ == "__main__":
    rospy.init_node("follow_and_obstacle_avoidance")
    listener = tf.TransformListener() 
    vel_pub = rospy.Publisher("robot2/cmd_vel_buf", Twist, queue_size=1)
    msg = Twist()
    rate = rospy.Rate(200.0)
    Xintegral = 0
    Xprevious_error = 0
    Yintegral = 0
    Yprevious_error = 0
    Aintegral = 0
    Aprevious_error = 0
    Kp = 10
    Ki = 0.5
    Kd = 1

    while not rospy.is_shutdown():
        t1 = time.time()
        Mot = rospy.wait_for_message("/robot2/motion", Motion)
        r1odom = rospy.wait_for_message("/robot1/odom", Odometry)
        r2odom = rospy.wait_for_message("/robot2/odom", Odometry)
#        Obs = rospy.wait_for_message("robot2/obstacle_avoid_cmd", Twist)
        Xerror = Mot.Vx
        Yerror = Mot.Vy
        Aerror = Mot.Wz
        OFFSET_FACTOR = 20 #30 * Kp * Xerror

        if (abs(r1odom.twist.twist.linear.x) > 0.01): 
            ysum1 = rospy.wait_for_message("/YSum1", Distance)
            ysum2 = rospy.wait_for_message("/YSum2", Distance)
            ysum3 = rospy.wait_for_message("/YSum3", Distance)
            compensate1 = rospy.wait_for_message("/compensate1", Float32)
            compensate2 = rospy.wait_for_message("/compensate2", Float32)
            yo = OFFSET_FACTOR * (C1_WEIGHT * ysum1.distance + C2_WEIGHT * ysum2.distance + C3_WEIGHT * ysum3.distance) - 0.5 * compensate1.data - 0.5 * compensate2.data
            print(yo)
            angularo = 0 - round(yo / D, 4)
        # elif r1odom.twist.twist.linear.x > 0.01: 
        #     ysum4 = rospy.wait_for_message("YSum4", Distance)
        #     ysum5 = rospy.wait_for_message("YSum5", Distance)
        #     ysum6 = rospy.wait_for_message("YSum6", Distance)
        #     yo = OFFSET_FACTOR * (C1_WEIGHT * ysum4.distance + C2_WEIGHT * ysum5.distance + C3_WEIGHT * ysum6.distance)
        #     print(yo)
        #     angularo = 0 - round(yo / D, 4)

        else:
            yo = 0
            angularo = 0

        t2 = time.time()

        if abs(Xerror) > 0.01:
            Xintegral = Xintegral + Xerror
        
        if abs(Yerror) > 0.01:
            Yintegral = Yintegral + Yerror
            
        if abs(Aerror) > 0.01:
            Aintegral = Aintegral + Aerror
        
        Xderivative = Xerror - Xprevious_error
        Yderivative = Yerror -Yprevious_error
        Aderivative = Aerror - Aprevious_error
        Xprevious_error = Xerror
        Yprevious_error = Yerror
        Aprevious_error = Aerror
        
        msg.linear.x = Kp * Xerror + Ki * Xintegral + Kd * Xderivative
        msg.linear.y = Kp * Yerror + Ki * Yintegral + yo + Kd * Yderivative
        msg.angular.z = Kp * Aerror + Ki * Aintegral + angularo + Kd * Aderivative
            
        
        vel_pub.publish(msg)
        
        rate.sleep()
        
        print(t2 - t1)



        
