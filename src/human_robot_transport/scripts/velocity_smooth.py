#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.12.21

@author: guoxiong
"""

import math
import rospy
from geometry_msgs.msg import Twist


def smoothing(inputTopicName):
    tst1 = rospy.wait_for_message(inputTopicName, Twist)
    rospy.sleep(rospy.Duration(0.005))
    tst2 = rospy.wait_for_message(inputTopicName, Twist)
    tst = Twist()
    # if (tst2.linear.x - tst1.linear.x > 0.05):
    #     tst.linear.x = tst1.linear.x + 0.05
    # elif (tst2.linear.x - tst1.linear.x < -0.05):
    #     tst.linear.x = tst1.linear.x - 0.05
    # else:
    #     tst.linear.x = tst2.linear.x

    tst.linear.x = tst2.linear.x

    if (tst2.linear.y - tst1.linear.y > 0.05):
        tst.linear.y = tst1.linear.y + 0.05
    elif (tst2.linear.y - tst1.linear.y < -0.05):
        tst.linear.y = tst1.linear.y - 0.05
    else:
        tst.linear.y = tst2.linear.y

    if (tst2.angular.z - tst1.angular.z > 0.05):
        tst.angular.z = tst1.angular.z + 0.05
    elif (tst2.angular.z - tst1.angular.z < -0.05):
        tst.angular.z = tst1.angular.z - 0.05
    else:
        tst.angular.z = tst2.angular.z

    return tst

if __name__ == "__main__":
    rospy.init_node("smothing")
    rate = rospy.Rate(200)
    pub = rospy.Publisher("/robot2/cmd_vel", Twist, queue_size = 1)
    while not rospy.is_shutdown():
        pub.publish(smoothing("/robot2/cmd_vel_buf"))
        rate.sleep()

