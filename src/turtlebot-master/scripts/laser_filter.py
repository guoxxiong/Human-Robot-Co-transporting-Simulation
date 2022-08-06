#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 22:55:08 2021

@author: guoxiong
"""


import rospy
import tf
from sensor_msgs.msg import LaserScan

import math

def get_LaserData(topic_name):
    laser_scan = rospy.wait_for_message(topic_name, LaserScan)
    return laser_scan
    
#def laser_filter(laser_data, filter_angular, filter_radius):
    
if __name__ == '__main__':
    rospy.init_node('laser_filter')
    listener = tf.TransformListener()
    rate = rospy.Rate(10.0)
    
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time()) #X轴朝前，Y轴朝左
            d = math.sqrt(trans[0] ** 2 + trans[1] ** 2) #d为两个机器人间的距离
            theta = math.atan2(trans[1], trans[0]) #theta为前方机器人相对于当前机器人的方位角，逆时针旋转为正
            laser_data = get_LaserData('/scan') #获取激光数据0.2-0.3s
            filter_range = [d - 0.2, d] #设置滤波距离区间，d为两个机器人间的距离
            print("theta: {}".format(str(theta)))
            print("filter_range: {}".format((str(filter_range[0]) + ", " + str(filter_range[1]))))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        rate.sleep()
    