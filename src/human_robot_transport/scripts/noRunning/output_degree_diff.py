#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 22:55:08 2021

@author: guoxiong
"""


import rospy
from sensor_msgs.msg import LaserScan
from human_robot_transport.msg import DegDiff
import numpy as np

def get_LaserData(topicName):
    laser_scan = rospy.wait_for_message(topicName, LaserScan)
    return laser_scan
    
#def laser_filter(laser_data, filter_angular, filter_radius):
    
if __name__ == "__main__":
    rospy.init_node("output_degree_forward_difference")
    deg_pub = rospy.Publisher("robot2/deg_diff", DegDiff, queue_size = 1)
    msg = DegDiff()
    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        laser_data = get_LaserData("robot2/fixed_scan") #获取激光数据0.2-0.3s
        a = np.array(laser_data.ranges)
        b = np.append(a[1:], a[0])
        forward_difference = b - a
        jump_detect = {"indices": [], "values": []}
        for i in range(len(forward_difference)):
            if abs(forward_difference[i]) > 0.5:
                jump_detect["indices"].append(i)
                jump_detect["values"].append(forward_difference[i])
        msg.indices = jump_detect["indices"]
        msg.values = jump_detect["values"]
        deg_pub.publish(msg)
        rate.sleep()
    