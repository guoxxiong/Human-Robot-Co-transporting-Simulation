#!/usr/bin/env python
#coding=utf-8

import rospy
import tf
import time
from obstacle import Obstacle

D = 0.5 #设置robot1与robot2之间的距离D
LIDAR_ERROR = 0.05
STOP_DISTANCE = 0.2
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR



if __name__ == '__main__':
    rospy.init_node('test')
    
    listener = tf.TransformListener()
    
    rate = rospy.Rate(2.0)
    while not rospy.is_shutdown():
        try:
            #得到以robot2为坐标原点的robot1的姿态信息(平移和旋转)
            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time()) #查看相对的tf,返回平移和旋转  turtle2跟着turtle1变换
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        
        s1 = time.time()
        obstacle = Obstacle(trans)
        msg = obstacle.obstacle()
        s2 = time.time()
        print (str(s2 - s1) + ' s')
        print (msg)
        rate.sleep()

