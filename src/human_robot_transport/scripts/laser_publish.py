#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 00:07:45 2021

@author: guoxiong
"""
import rospy
from sensor_msgs.msg import LaserScan

scan_range_pub1 = rospy.Publisher("robot2/scan1", LaserScan, queue_size = 1)
scan_range_pub2 = rospy.Publisher("robot2/scan2", LaserScan, queue_size = 1)
scan_range_pub3 = rospy.Publisher("robot2/scan3", LaserScan, queue_size = 1)

def laser_callback1(data):
    scan_range_pub1.publish(data)
    
def laser_callback2(data):
    scan_range_pub2.publish(data)
    
def laser_callback3(data):
    scan_range_pub3.publish(data)



if __name__ == "__main__":
    rospy.init_node("laser_publish")
    rospy.Subscriber("robot2/scan", LaserScan, laser_callback1)
    rospy.Subscriber("robot2/scan", LaserScan, laser_callback2)
    rospy.Subscriber("robot2/scan", LaserScan, laser_callback3)
    rospy.spin()
