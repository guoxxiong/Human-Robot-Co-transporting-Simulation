#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:45:35 2021

@author: guoxiong
"""


import rospy
import tf
import csv
import time
import math
from nav_msgs.msg import Odometry


    
def get_robot_speed_and_distance():

#    robot1_x = []
#    robot1_y = []
#    robot2_x = []
#    robot2_y = []    
    t = time.time()
    f1 = open("robot_speed_and_distance" + str(int(t)) + ".csv", "w")
    writer1 = csv.writer(f1)
    
    listener = tf.TransformListener()
    rate = rospy.Rate(100.0)
    t1 = time.time()
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform("/robot2/odom", "/robot1/odom", rospy.Time())
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        data = []
        odom = rospy.wait_for_message("robot2/odom", Odometry)
        t2 = time.time()
        data.append(round(0.1*(t2 - t1), 4))
        data.append(round(odom.twist.twist.linear.x, 4))
        data.append(round(odom.twist.twist.linear.y, 4))
        data.append(round(odom.twist.twist.angular.z, 4))
        data.append(round(math.sqrt(trans[0]**2 + trans[1]**2), 4))
        writer1.writerow(data)
        rate.sleep()
        
    f1.close()

    
if __name__ == "__main__":
    rospy.init_node("get_robot_speed_and_distance")
    get_robot_speed_and_distance()
    rospy.spin()
