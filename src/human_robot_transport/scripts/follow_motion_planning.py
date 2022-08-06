#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 23:48:57 2021

@author: guoxiong
"""


import rospy
from human_robot_transport.msg import NextPose
from human_robot_transport.msg import Motion
import math
import numpy as np

pub = rospy.Publisher("robot2/motion", Motion, queue_size = 1)

def motion_planning(z):
    Mot = Motion()
    AC = math.sqrt(z.x**2 + z.y**2)
    RAC = math.fabs(0.5 * AC / (math.sin(0.5*z.theta)))
    LAC = math.fabs(z.theta) * RAC
    Vx = math.fabs(LAC * math.cos(0.5*z.theta)) * np.sign(z.x)
    Vy = math.fabs(LAC * math.sin(0.5*z.theta)) * np.sign(z.y)
#    Vx = AC * np.sign(z.x)
#    Vy = 0
    Mot.Vx = Vx
    Mot.Vy = Vy
    Mot.Wz = z.theta
    print(Mot)
    pub.publish(Mot)
    
    
    
    
if __name__ == "__main__":
    rospy.init_node("follow_motion_planning")
    sub = rospy.Subscriber("/robot2NextState", NextPose, motion_planning)
    rospy.spin()
    