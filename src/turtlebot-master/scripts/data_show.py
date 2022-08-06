#!/usr/bin/env python
#coding=utf-8

import rospy
#import math
#from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

#def get_scan():
#        scan = rospy.wait_for_message('robot2/scan', LaserScan)
#        scan_filter = []
#       
#        samples = len(scan.ranges)  # The number of samples is defined in 
#                                    # turtlebot3_<model>.gazebo.xacro file,
#                                    # the default is 360.
#        samples_view = 360           # 1 <= samples_view <= samples
#        
#        if samples_view > samples:
#            samples_view = samples
#
#        if samples_view is 1:
#            scan_filter.append(scan.ranges[0])
#
#        else:
#            scan_filter = list(scan.ranges)
#
#
#        for i in range(samples_view):
#            if scan_filter[i] == float('Inf'):
#                scan_filter[i] = 3.5
#            elif math.isnan(scan_filter[i]):
#                scan_filter[i] = 0
#        
#        return min(scan_filter), (450 - (180 - (scan_filter.index(min(scan_filter)) - 179)))%360
#
#def convert_scan(d, theta):
#        x = d * math.cos(math.pi * round(theta / 180.0, 3))
#        y = d * math.sin(math.pi * round(theta / 180.0, 3))
#        return round(x, 3), round(y, 3)

def get_r1_cmd_vel():
    return rospy.wait_for_message('robot1/cmd_vel', Twist, timeout = None)

if __name__ == '__main__':
#    rospy.init_node('data_show')
#
#    listener = tf.TransformListener() #TransformListener创建后就开始接受tf广播信息，最多可以缓存10s
#
#    '''
#    #设置robot2的初始坐标
#    robot2_start = rospy.Publisher('robot2/odom', nav_msgs/Odometry, queue_size=1)
#    msg.pose.pose.position.x = 0
#    msg.pose.pose.position.y = 0
#    msg.pose.pose.position.z = 0
#    msg.pose.pose.orientation.x = 0
#    msg.pose.pose.orientation.y = 0
#    msg.pose.pose.orientation.z = 0
#    msg.pose.pose.orientation.w = 0
#    robot2_start.publish(msg) #将请求的参数传入  robot2的初始位置
#    '''
#
#    #Publisher 函数第一个参数是话题名称，第二个参数 数据类型，现在就是我们定义的msg 最后一个是缓冲区的大小
#
#    rate = rospy.Rate(10.0) #循环执行，更新频率是10hz
#    while not rospy.is_shutdown():
#        try:
#            #得到以robot2为坐标原点的robot1的姿态信息(平移和旋转)
#            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time()) #查看相对的tf,返回平移和旋转  turtle2跟着turtle1变换
#            (d, theta) = get_scan()
#            (x2, y2) = convert_scan(d, theta)
#        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
#            continue
#	print "the distance and angular of the obstacle: "
#	print round(d, 3), theta
#	print "the axis of the obstacle: "
#	print x2, y2
#        angular = math.atan2(trans[1], trans[0]) #角度变换 计算出前往robot1的角速度 atan2(double y,double x) 返回的是原点至点(x,y)的方位角，即与 x 轴的夹角
#        linear = math.sqrt(trans[0] ** 2 + trans[1] ** 2) #平移变换 计算出前往robot1的线速度
#        rate.sleep() #以固定频率执行
        
    rospy.init_node('data_show')
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        print(get_r1_cmd_vel())
        rate.sleep()