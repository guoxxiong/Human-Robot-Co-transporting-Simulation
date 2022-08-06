import threading
import numpy as np
#!/usr/bin/env python
#coding=utf-8
"""
Created on Wed Apr 14 22:58:08 2021

@author: guoxiong
"""

from matplotlib import pyplot as plt
import rospy
from nav_msgs.msg import Odometry

arrayLength = 100
angularspeed = np.zeros(arrayLength)


def speed_get_process():
    rate = rospy.Rate(100.0)
    odm = Odometry()
    i = 0
    while not rospy.is_shutdown():
        odm = rospy.wait_for_message("/robot2/odom", Odometry)
        if i < arrayLength:
            angularspeed[i] = odm.twist.twist.angular.z
            i = i + 1
        else:
            angularspeed[:-1] = angularspeed[1:]
            angularspeed[i-1] = odm.twist.twist.angular.z
        rate.sleep()

    
def angular_speed_plot():
    plt.grid(True)
    plt.xlabel("time(s)")
    plt.ylabel("angular speed(rad/s)")
    plt.xlim((0, 100))
    plt.ylim((-1, 1))
    my_y_ticks = np.arange(-1, 1, 0.2)
    plt.yticks(my_y_ticks)
    while True:
        plt.clf()
        plt.plot(angularspeed, color = "c")
        plt.grid(True)
        plt.xlim((0, 100))
        plt.ylim((-1, 1))
        plt.yticks(my_y_ticks)
        plt.xlabel("time(unit: 20ms)")
        plt.ylabel("angular speed(rad/s)")
        plt.legend(labels = ["angular speed around Z axis"])
        plt.pause(0.02)
        
if __name__ == "__main__":
    rospy.init_node("angular_speed_plot")
    th1 = threading.Thread(target = speed_get_process)
    th2 = threading.Thread(target = angular_speed_plot)
    
    th1.start()
    th2.start()

    th1.join()
    th2.join()
  
    rospy.spin()