#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 16:44:02 2021

@author: guoxiong
"""


import rospy
from geometry_msgs.msg import Twist


if __name__ == "__main__":
    rospy.init_node("cmd_pub")
    pub = rospy.Publisher("robot2/cmd_vel", Twist, queue_size = 1)
    twist = Twist()
    rate = rospy.Rate(400.0)
    while not rospy.is_shutdown():
        twist1 = rospy.wait_for_message("robot2/follow_cmd", Twist)
        twist2 = rospy.wait_for_message("robot2/obstacle_avoid_cmd", Twist)
        twist.linear.x = twist1.linear.x + 0 * twist2.linear.x
        twist.linear.y = twist1.linear.y + 0 * twist2.linear.y
        twist.angular.z = twist1.angular.z + 0 * twist2.angular.z
        print(twist)
        pub.publish(twist)
        rate.sleep()