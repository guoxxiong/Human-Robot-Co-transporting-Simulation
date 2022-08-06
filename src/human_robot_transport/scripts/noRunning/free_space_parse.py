#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 12:45:15 2021

@author: guoxiong
"""


import rospy
from human_robot_transport.msg import DegDiff, FreeSpace


def get_deg_grad(topicName):
    deg_grad = rospy.wait_for_message(topicName, DegDiff)
    return deg_grad

def find_deg_of_free_space(deg_diff):
    degrees_list = list(deg_diff.indices)
    value_list = list(deg_diff.values)
    if value_list:
    	next_value_list = value_list[1:]
    	next_value_list.append(value_list[0])
    	start_deg = []
    	end_deg = []
    	connected = {"start": [], "end": []}
    	# Rising Edge and Falling Edge Detect
    	for i in range(len(value_list)):
        	if (value_list[i] < 0) and (next_value_list[i] > 0):
        	    if i < len(value_list) - 1:
            		start_deg.append(degrees_list[i+1])
            		end_deg.append(degrees_list[i])
        	    elif i == len(value_list) - 1:
            		start_deg.append(degrees_list[0])
            		end_deg.append(degrees_list[i])
    	# Connect start_deg with end_deg
    	for e in end_deg:
            difference = 360
            for s in start_deg:
                if (e > s) and ((e - s) < difference):
                    difference = e - s
                    temp_s = s
                elif (e < s) and ((e - s + 360) < difference):
                    difference = e - s + 360
                    temp_s = s
    	connected["start"].append(temp_s)
    	connected["end"].append(e)
    	return connected
    
if __name__ == "__main__":
    rospy.init_node("free_space_parse")
    rate = rospy.Rate(10.0)
    free_space_pub = rospy.Publisher("robot2/free_space"人, FreeSpace, queue_size = 1)
    msg = FreeSpace()
    while not rospy.is_shutdown():
        deg_diff = get_deg_grad("robot2/deg_diff")
        free_deg = find_deg_of_free_space(deg_diff)
        if not free_deg == None:
            msg.start = free_deg["start"]
            msg.end = free_deg["end"]
        free_space_pub.publish(msg)
        rate.sleep()
