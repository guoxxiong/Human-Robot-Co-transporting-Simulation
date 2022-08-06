#!/usr/bin/env python
#coding=utf-8
"""
Created on Wed Apr 14 22:58:08 2021

@author: guoxiong
"""
import threading
import math
import numpy as np
from matplotlib import pyplot as plt
import rospy
import tf
from human_robot_transport.msg import Distance

arrayLength = 100
dist =  np.zeros(arrayLength)


def dist_get_and_pub():
    listener = tf.TransformListener()
    distance_pub = rospy.Publisher("distance", Distance, queue_size = 1)
    rate = rospy.Rate(100.0)
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform("/robot2/odom", "/robot1/odom", rospy.Time())
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        distance = round(math.sqrt(trans[0]**2 + trans[1]**2), 3)
        distance_pub.publish(distance)
        rate.sleep()
       
        
def dist_process():
    rate = rospy.Rate(100.0)
    i = 0
    while not rospy.is_shutdown():
        distance = rospy.wait_for_message("distance", Distance)
        if i < arrayLength:
            dist[i] = distance.distance
            i = i + 1
        else:
            dist[:-1] = dist[1:]
            dist[i-1] = distance.distance
        rate.sleep()
        
        
def distance_plot():
    plt.grid(True)
    plt.xlabel("time(s)")
    plt.ylabel("distance(m)")
    plt.xlim((0, 100))
    plt.ylim((1.1, 1.3))
    my_y_ticks = np.arange(1.1, 1.3, 0.02)
    desired__distance = np.ones(100) * 1.2
    plt.yticks(my_y_ticks)
    while True:
        plt.clf()
        plt.grid(True)
        plt.xlabel("time(unit: 10ms)")
        plt.ylabel("distance(m)")
        plt.xlim((0, 100))
        plt.ylim((1.1, 1.3))
        plt.yticks(my_y_ticks)
        plt.plot(dist, color = "b", linewidth = 3)
        plt.plot(desired__distance, color = "r", linewidth =2, linestyle = "--")
        plt.legend(labels = ["actual distance", "desired distance"])
        plt.pause(0.02)
        

    
if __name__ == "__main__":
    rospy.init_node("distance_plot")
    th1 = threading.Thread(target = dist_get_and_pub)
    th2 = threading.Thread(target = dist_process)
    th3 = threading.Thread(target = distance_plot)

    th1.start()
    th2.start()
    th3.start()


    th1.join()
    th2.join()
    th3.join()

    rospy.spin()
