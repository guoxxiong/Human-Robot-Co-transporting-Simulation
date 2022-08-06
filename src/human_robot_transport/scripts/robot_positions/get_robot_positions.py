#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 15:17:49 2021

@author: guoxiong
"""


import rospy
from nav_msgs.msg import Odometry
import csv
import time

def get_robot_position():

#    robot1_x = []
#    robot1_y = []
#    robot2_x = []
#    robot2_y = []    
    t = time.time()
    f1 = open("SCE1/robot1_xy" + str(int(t)) + ".csv", "w")
    f2 = open("SCE1/robot2_xy" + str(int(t)) + ".csv", "w")
    writer1 = csv.writer(f1)
    writer2 = csv.writer(f2)
    
    rate = rospy.Rate(100.0)
    odom1 = Odometry()
    odom2 = Odometry()

    while not rospy.is_shutdown():
        robot1_xy = []
        robot2_xy = []
        odom1 = rospy.wait_for_message("robot1/odom", Odometry)
        odom2 = rospy.wait_for_message("robot2/odom", Odometry)
        robot1_xy.append(odom1.pose.pose.position.x)
        robot1_xy.append(odom1.pose.pose.position.y)
        robot2_xy.append(odom2.pose.pose.position.x)
        robot2_xy.append(odom2.pose.pose.position.y)
        writer1.writerow(robot1_xy)
        writer2.writerow(robot2_xy)
        rate.sleep()

    f1.close()
    f2.close()

    
if __name__ == "__main__":
    rospy.init_node("get_robot_position")
    get_robot_position()
    rospy.spin()
