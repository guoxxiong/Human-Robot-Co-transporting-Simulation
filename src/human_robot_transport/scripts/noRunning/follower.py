#!/usr/bin/env python
#coding=utf-8
"""
Created on Wed Apr 14 22:58:08 2021

@author: guoxiong
"""


import rospy
import tf
from geometry_msgs.msg import Twist
from human_robot_transport.msg import Motion


if __name__ == "__main__":
    rospy.init_node("follower")
    listener = tf.TransformListener() 
    vel_pub = rospy.Publisher("robot2/cmd_vel", Twist, queue_size=1)
    msg = Twist()
    rate = rospy.Rate(100.0)
    Xintegral = 0
    Xprevious_error = 0
    Yintegral = 0
    Yprevious_error = 0
    Aintegral = 0
    Aprevious_error = 0
    Kp = 91
    Ki = 0
    Kd = 0

    while not rospy.is_shutdown():
#        t1 = time.time()
#        try:
#            
#            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time())
#        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
#            continue
#	
#        angular = math.atan2(trans[1], trans[0]) 
#        distance = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
#        Xerror = trans[0] * (distance - D) / distance
#        Yerror = trans[1] * (distance - D) / distance
#        print(Xerror)
#        print(Yerror)
#        print(angular)
        Mot = rospy.wait_for_message("robot2/motion", Motion)
        twist = rospy.wait_for_message("robot2/cmd_vel", Twist)
#       Obs = rospy.wait_for_message("robot2/obstacle_avoid_cmd", Twist)
        Xerror = Mot.Vx
        Yerror = Mot.Vy
        Aerror = Mot.Wz
        
        if abs(Xerror) > 0.001:
            Xintegral = Xintegral + Xerror
        
        if abs(Yerror) > 0.001:
            Yintegral = Yintegral + Yerror
            
        if abs(Aerror) > 0.005:
            Aintegral = Aintegral + Aerror
        
        Xderivative = Xerror - Xprevious_error
        Yderivative = Yerror -Yprevious_error
        Aderivative = Aerror - Aprevious_error
        Xprevious_error = Xerror
        Yprevious_error = Yerror
        Aprevious_error = Aerror
        
        msg.linear.x = Kp * Xerror + Ki * Xintegral + Kd * Xderivative
        msg.linear.y = Kp * Yerror + Ki * Yintegral + Kd * Yderivative 
        msg.angular.z = Kp * Aerror + Ki * Aintegral + Kd * Aderivative
            
        
        vel_pub.publish(msg)
        print(msg)
        rate.sleep()



        
