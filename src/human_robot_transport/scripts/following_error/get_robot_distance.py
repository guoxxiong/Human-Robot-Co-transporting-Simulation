#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 15:17:49 2021

@author: guoxiong
"""


import rospy
import tf
import csv
import time
import math

def get_robot_distance():

#    robot1_x = []
#    robot1_y = []
#    robot2_x = []
#    robot2_y = []    
    t = time.time()
    f1 = open("robot12_distance" + str(int(t)) + ".csv", "w")
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
        t2 = time.time()
        data.append(round(0.1 * (t2 - t1), 3))
        data.append(round(math.sqrt(trans[0]**2 + trans[1]**2), 3))
        writer1.writerow(data)
        rate.sleep()
        
    f1.close()

    
if __name__ == "__main__":
    rospy.init_node("get_robot_distance")
    get_robot_distance()
    rospy.spin()
