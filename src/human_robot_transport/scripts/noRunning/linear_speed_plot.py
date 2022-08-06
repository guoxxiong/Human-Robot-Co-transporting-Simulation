#!/usr/bin/env python
#coding=utf-8
"""
Created on Wed Apr 14 22:58:08 2021

@author: guoxiong
"""

import threading
import numpy as np
from matplotlib import pyplot as plt
import rospy
from nav_msgs.msg import Odometry

arrayLength = 100
xspeed = np.zeros(arrayLength)
yspeed = np.zeros(arrayLength)


def speed_get_process():
    rate = rospy.Rate(100.0)
    odm = Odometry()
    i = 0
    while not rospy.is_shutdown():
        odm = rospy.wait_for_message("/robot2/odom", Odometry)
        if i < arrayLength:
            xspeed[i] = odm.twist.twist.linear.x
            yspeed[i] = odm.twist.twist.linear.y
            i = i + 1
        else:
            xspeed[:-1] = xspeed[1:]
            xspeed[i-1] = odm.twist.twist.linear.x
            yspeed[:-1] = yspeed[1:]
            yspeed[i-1] = odm.twist.twist.linear.y
        rate.sleep()

    
def linear_speed_plot():
    plt.grid(True)
    plt.xlabel("time(s)")
    plt.ylabel("speed(m/s)")
    plt.xlim((0, 100))
    plt.ylim((-1.5, 1.5))
    my_y_ticks = np.arange(-1.5, 1.5, 0.2)
    plt.yticks(my_y_ticks)
    while True:
        plt.clf()
        plt.plot(xspeed, color = "r")
        plt.plot(yspeed, color = "g")
        plt.xlim((0, 100))
        plt.ylim((-1.5, 1.5))
        plt.yticks(my_y_ticks)
        plt.grid(True)
        plt.xlabel("time(unit: 10ms)")
        plt.ylabel("speed(m/s)")
        plt.legend(labels = ["X axis speed", "Y axis speed"])
        plt.pause(0.02)
        
if __name__ == "__main__":
    rospy.init_node("linear_speed_plot")
    th1 = threading.Thread(target = speed_get_process)
    th2 = threading.Thread(target = linear_speed_plot)
    
    th1.start()
    th2.start()

    th1.join()
    th2.join()
  
    rospy.spin()