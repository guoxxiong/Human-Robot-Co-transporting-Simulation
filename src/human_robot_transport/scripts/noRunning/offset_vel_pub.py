#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 21:34:55 2021

@author: guoxiong
"""


import rospy
import tf
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from human_robot_transport.msg import FreeSpace

import math

OFFSET_FACTOR = 1
OFFSET_TRIG_DISTANCE = 4
D = 1.2



def y_velocity_parse(free_space, human_odom, laser_data, angle_h_r):
    forward_distance = {"start":[], "end":[]}
    backward_distance = {"start":[], "end":[]}
    forward_angle = {"start":[], "end":[]}
    backward_angle = {"start":[], "end":[]}
    msg = Twist()
    forward_select_factor = 2 *(OFFSET_TRIG_DISTANCE - D)
    backward_select_factor = 2 *(OFFSET_TRIG_DISTANCE - D)
    
    for i in range(len(free_space.start)):
        if ((free_space.start[i] < 90) or (free_space.start[i] > 270)) and\
        ((free_space.end[i] < 90) or (free_space.end[i] > 270)):
            forward_distance["start"].append(laser_data.ranges[free_space.start[i]])
            forward_angle["start"].append(free_space.start[i])
            forward_distance["end"].append(laser_data.ranges[free_space.end[i]])
            forward_angle["end"].append(free_space.end[i])
        elif ((free_space.start[i] > 90) and (free_space.start[i] < 270)) and\
        ((free_space.end[i] > 90) and (free_space.end[i] < 270)):
            backward_distance["start"].append(laser_data.ranges[free_space.start[i]])
            backward_angle["start"].append(free_space.start[i])
            backward_distance["end"].append(laser_data.ranges[free_space.end[i]])
            backward_angle["start"].append(free_space.end[i])
            
    forward_index_flag = 0
    backward_index_flag = 0
    # Search the nearest convex of forward
    for i in range(len(forward_distance["start"])):
        if (forward_distance["start"][i] + forward_distance["end"][i] - 2 * D) < forward_select_factor:
            forward_select_factor = forward_distance["start"][i] + forward_distance["end"][i] - 2 * D
            forward_index_flag = i
    # Search the nearest convex of backward
    for i in range(len(backward_distance["start"])):
        if (backward_distance["start"][i] + backward_distance["end"][i]) < backward_select_factor:
            backward_select_factor = backward_distance["start"][i] + backward_distance["end"][i]
            backward_index_flag = i
            
    if (forward_angle["start"][forward_index_flag]) > 270:
        forward_angle["start"][forward_index_flag] = forward_angle["start"][forward_index_flag] - 360
    elif (forward_angle["end"][forward_index_flag]) > 270:
        forward_angle["end"][forward_index_flag] = forward_angle["end"][forward_index_flag] - 360
        
    if (forward_select_factor < backward_select_factor) and\
    (angle_h_r > forward_angle["start"][forward_index_flag] and\
     angle_h_r < forward_angle["end"][forward_index_flag]):
        msg.linear.y = (forward_distance["end"][forward_index_flag] - \
                        forward_distance["start"][forward_index_flag]) * OFFSET_FACTOR
        
    elif (forward_select_factor > backward_select_factor) and\
    (angle_h_r + 180 > backward_angle["start"][backward_index_flag] and\
     angle_h_r + 180 < backward_angle["end"][backward_index_flag]):
        msg.linear.y = 0 - (backward_distance["end"][backward_index_flag] - \
                        backward_distance["start"][backward_index_flag]) * OFFSET_FACTOR
                        
    print(forward_select_factor)
    print(backward_select_factor)                        
    print(forward_angle)
    print(forward_distance)    
    return msg
            
    
    

if __name__ == "__main__":
    rospy.init_node("offset_vel_pub")
    vel_pub = rospy.Publisher("robot2/cmd_vel", Twist, queue_size = 1)
    listener = tf.TransformListener()
    rate = rospy.Rate(5.0)
    
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time())
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        angle_h_r = math.atan2(trans[1], trans[0])
        free_space = rospy.wait_for_message("robot2/free_space", FreeSpace)
        human_odom = rospy.wait_for_message("robot1/odom", Odometry)
        laser_data = rospy.wait_for_message("robot2/fixed_scan", LaserScan)
        y_offset_msg = y_velocity_parse(free_space, human_odom, laser_data, angle_h_r)
        #print(y_offset_msg)
        vel_pub.publish(y_offset_msg)
        rate.sleep()
    