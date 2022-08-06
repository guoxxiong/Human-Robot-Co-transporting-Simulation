#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 00:07:45 2021

@author: guoxiong
"""
import rospy
from sensor_msgs.msg import LaserScan


THRESH1 = 2
THRESH2 = 1
THRESH3 = 0.5

inf = float("inf")

scan_range_pub1 = rospy.Publisher("robot2/fixed_scan1", LaserScan, queue_size = 1)
scan_range_pub2 = rospy.Publisher("robot2/fixed_scan2", LaserScan, queue_size = 1)
scan_range_pub3 = rospy.Publisher("robot2/fixed_scan3", LaserScan, queue_size = 1)
# scan_range_pub4 = rospy.Publisher("robot2/fixed_scan4", LaserScan, queue_size = 1)
# scan_range_pub5 = rospy.Publisher("robot2/fixed_scan5", LaserScan, queue_size = 1)
# scan_range_pub6 = rospy.Publisher("robot2/fixed_scan6", LaserScan, queue_size = 1)

def laser_callback1(data):
    temp = list(data.ranges)
    for i in range(len(temp)):
        if (temp[i] == inf) or (temp[i] > THRESH1):
            temp[i] = THRESH1
    # for i in range(len(temp)):
    #     if (temp[i] == inf) or (temp[i] > THRESH1) or (temp[i] < THRESH2):
    #         temp[i] = THRESH1
    # for i in range(0, int(len(temp)/4)-15):
    #     if (temp[i] == inf) or (temp[i] > THRESH1):
    #         temp[i] = THRESH1
    # for i in range(int(3 * (len(temp)/4))+15, len(temp)):
    #     if (temp[i] == inf) or (temp[i] > THRESH1):
    #         temp[i] = THRESH1
    # for i in range(int(len(temp)/4)-15, int(3 * (len(temp)/4))+15):
    #         temp[i] = 2.7
    data.ranges = tuple(temp)
    scan_range_pub1.publish(data)
    
def laser_callback2(data):
    temp = list(data.ranges)
    for i in range(len(temp)):
        if (temp[i] == inf) or (temp[i] > THRESH2):
            temp[i] = THRESH2
    # for i in range(len(temp)):
    #     if (temp[i] == inf) or (temp[i] > THRESH2) or (temp[i] < THRESH3):
    #         temp[i] = THRESH2
    # for i in range(0, int(len(temp)/4)-15):
    #     if (temp[i] == inf) or (temp[i] > THRESH2):
    #         temp[i] = THRESH2
    # for i in range(int(3 * (len(temp)/4))+15, len(temp)):
    #     if (temp[i] == inf) or (temp[i] > THRESH2):
    #         temp[i] = THRESH2
    # for i in range(int(len(temp)/4)-15, int(3 * (len(temp)/4))+15):
    #         temp[i] = 1.8
    data.ranges = tuple(temp)
    scan_range_pub2.publish(data)
    
def laser_callback3(data):
    temp = list(data.ranges)
    for i in range(len(temp)):
        if (temp[i] == inf) or (temp[i] > THRESH3):
            temp[i] = THRESH3
    # for i in range(len(temp)):
    #     if (temp[i] == inf) or (temp[i] > THRESH3):
    #         temp[i] = THRESH3
    # for i in range(0, int(len(temp)/4)-15):
    #     if (temp[i] == inf) or (temp[i] > THRESH3):
    #         temp[i] = THRESH3
    # for i in range(int(3 * (len(temp)/4))+15, len(temp)):
    #     if (temp[i] == inf) or (temp[i] > THRESH3):
    #         temp[i] = THRESH3
    # for i in range(int(len(temp)/4)-15, int(3 * (len(temp)/4))+15):
    #         temp[i] = 0.9
    data.ranges = tuple(temp)
    scan_range_pub3.publish(data)

# def laser_callback4(data):
#     temp = list(data.ranges)
#     for i in range(0, int(len(temp)/4)+15):
#         temp[i] = 2.7
#     for i in range(int(3 * (len(temp)/4))-15, len(temp)):
#         temp[i] = 2.7
#     for i in range(int(len(temp)/4)+15, int(3 * (len(temp)/4))-15):
#         if (temp[i] == inf) or (temp[i] > THRESH1):
#             temp[i] = THRESH1
#     data.ranges = tuple(temp)
#     scan_range_pub4.publish(data)

# def laser_callback5(data):
#     temp = list(data.ranges)
#     for i in range(0, int(len(temp)/4)+15):
#         temp[i] = 1.8
#     for i in range(int(3 * (len(temp)/4))-15, len(temp)):
#         temp[i] = 1.8
#     for i in range(int(len(temp)/4)+15, int(3 * (len(temp)/4))-15):
#         if (temp[i] == inf) or (temp[i] > THRESH2):
#             temp[i] = THRESH2
#     data.ranges = tuple(temp)
#     scan_range_pub5.publish(data)

# def laser_callback6(data):
#     temp = list(data.ranges)
#     for i in range(0, int(len(temp)/4)+15):
#         temp[i] = 0.9
#     for i in range(int(3 * (len(temp)/4))-15, len(temp)):
#         temp[i] = 0.9
#     for i in range(int(len(temp)/4)+15, int(3 * (len(temp)/4))-15):
#         if (temp[i] == inf) or (temp[i] > THRESH3):
#             temp[i] = THRESH3
#     data.ranges = tuple(temp)
#     scan_range_pub6.publish(data)



if __name__ == "__main__":
    rospy.init_node("laser_fix")
    rospy.Subscriber("robot2/scan1", LaserScan, laser_callback1)
    rospy.Subscriber("robot2/scan2", LaserScan, laser_callback2)
    rospy.Subscriber("robot2/scan3", LaserScan, laser_callback3)
    # rospy.Subscriber("robot2/scan", LaserScan, laser_callback4)
    # rospy.Subscriber("robot2/scan", LaserScan, laser_callback5)
    # rospy.Subscriber("robot2/scan", LaserScan, laser_callback6)
    rospy.spin()
