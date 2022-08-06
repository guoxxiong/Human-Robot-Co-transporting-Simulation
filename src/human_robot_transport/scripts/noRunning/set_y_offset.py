#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 20:38:57 2021

@author: guoxiong
"""


#!/usr/bin/env python
#coding=utf-8
"""
Created on Wed Apr 14 22:58:08 2021

@author: guoxiong
"""


import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from human_robot_transport.msg import Distance
from parameters import W_v_1
from parameters import D


class pub_y_offset_vel():
    def __init__(self):
        self.OFFSET_FACTOR = 0.1
        self.C1_weight = 0.125
        self.C2_weight = 0.3
        self.C3_weight = 0.575
        self.vy1 = 0
        self.vy2 = 0
        self.vy3 = 0
        self.sub1 = rospy.Subscriber("/YSum1", Distance, self.pubcallback1)
        self.sub2 = rospy.Subscriber("/YSum2", Distance, self.pubcallback2)
        self.sub3 = rospy.Subscriber("/YSum3", Distance, self.pubcallback3)
        self.pub = rospy.Publisher("robot2/cmd_vel", Twist, queue_size = 1)
        self.publish_vy()
        
    def pubcallback1(self, data):
        self.vy1 = self.C1_weight * self.OFFSET_FACTOR * data.distance
        
    def pubcallback2(self, data):
        self.vy2 = self.C2_weight * self.OFFSET_FACTOR * data.distance
       
    def pubcallback3(self, data):
        self.vy3 = self.C3_weight * self.OFFSET_FACTOR * data.distance
        
    def publish_vy(self):
        msg = Twist()
        rate = rospy.Rate(400.0)
        while not  rospy.is_shutdown():
            odom1 = rospy.wait_for_message("robot1/odom", Odometry)
            twist = rospy.wait_for_message("robot2/cmd_vel", Twist)
            if (abs(odom1.twist.twist.linear.x) > 0.05) or (abs(odom1.twist.twist.linear.y) > 0.05):
                vy = self.vy1 + self.vy2 + self.vy3
                w = round((0 - vy) / D, 3)
                msg.linear.x = twist.linear.x
                msg.linear.y = vy
                msg.angular.z = w
                self.pub.publish(msg)
            else:
                vy = 0
                w = 0
                msg.linear.y = vy
                msg.angular.z = w
                self.pub.publish(msg)
            rate.sleep()


if __name__ == "__main__":
    rospy.init_node("set_y_offset")
    pubYVel = pub_y_offset_vel()
    rospy.spin()
