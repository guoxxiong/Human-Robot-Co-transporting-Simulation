#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:17:19 2021

@author: guoxiong
"""


#!/usr/bin/env python
#coding=utf-8
"""
Created on Wed Apr 14 22:58:08 2021

@author: guoxiong
"""


import rospy
import math
import tf
from geometry_msgs.msg import Twist

D = 1.2 #设置robot1与robot2之间的距离D


if __name__ == "__main__":
    rospy.init_node("follower")

    listener = tf.TransformListener() #TransformListener创建后就开始接受tf广播信息，最多可以缓存10s

    #Publisher 函数第一个参数是话题名称，第二个参数 数据类型，现在就是我们定义的msg 最后一个是缓冲区的大小
    vel_pub = rospy.Publisher("robot2/cmd_vel", Twist, queue_size=1)
    msg = Twist()
    rate = rospy.Rate(100.0) #循环执行，更新频率是10hz
    while not rospy.is_shutdown():
        try:
            #得到以robot2为坐标原点的robot1的姿态信息(平移和旋转)
            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time()) #查看相对的tf,返回平移和旋转  turtle2跟着turtle1变换
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        print(trans)
        rate.sleep() #以固定频率执行
        
