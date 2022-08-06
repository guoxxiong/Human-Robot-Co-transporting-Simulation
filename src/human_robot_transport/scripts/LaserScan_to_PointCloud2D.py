#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 13:05:30 2021

@author: guoxiong
"""

import rospy
from sensor_msgs.msg import PointCloud2 as pc2
from sensor_msgs import point_cloud2
from sensor_msgs.msg import LaserScan
from human_robot_transport.msg import Distance 
from laser_geometry import LaserProjection
import numpy as np

class Laser2PC2YSum():
    def __init__(self):
        self.laserProj = LaserProjection()
        self.pcPub1 = rospy.Publisher("/PointCloud1", pc2, queue_size=1)
        self.pcPub2 = rospy.Publisher("/PointCloud2", pc2, queue_size=1)
        self.pcPub3 = rospy.Publisher("/PointCloud3", pc2, queue_size=1)
        # self.pcPub4 = rospy.Publisher("/PointCloud4", pc2, queue_size=1)
        # self.pcPub5 = rospy.Publisher("/PointCloud5", pc2, queue_size=1)
        # self.pcPub6 = rospy.Publisher("/PointCloud6", pc2, queue_size=1)
        self.sumPub1 = rospy.Publisher("/YSum1", Distance, queue_size=1)
        self.sumPub2 = rospy.Publisher("/YSum2", Distance, queue_size=1)
        self.sumPub3 = rospy.Publisher("/YSum3", Distance, queue_size=1)
        # self.sumPub4 = rospy.Publisher("/YSum4", Distance, queue_size=1)
        # self.sumPub5 = rospy.Publisher("/YSum5", Distance, queue_size=1)
        # self.sumPub6 = rospy.Publisher("/YSum6", Distance, queue_size=1)
        self.laserSub1 = rospy.Subscriber("robot2/fixed_scan1", LaserScan, self.laserCallback1)
        self.laserSub2 = rospy.Subscriber("robot2/fixed_scan2", LaserScan, self.laserCallback2)
        self.laserSub3 = rospy.Subscriber("robot2/fixed_scan3", LaserScan, self.laserCallback3)
        # self.laserSub4 = rospy.Subscriber("robot2/fixed_scan4", LaserScan, self.laserCallback4)
        # self.laserSub5 = rospy.Subscriber("robot2/fixed_scan5", LaserScan, self.laserCallback5)
        # self.laserSub6 = rospy.Subscriber("robot2/fixed_scan6", LaserScan, self.laserCallback6)

    def laserCallback1(self,data):
        cloud_out = self.laserProj.projectLaser(data)
        position = point_cloud2.read_points(cloud_out, field_names=("y"))
        position_array = list(position)
        position_array = np.array(position_array)
        y_abs_sum = sum(abs(position_array))
        y_sum = sum(position_array) / y_abs_sum
        self.pcPub1.publish(cloud_out)
        self.sumPub1.publish(y_sum)
        
    def laserCallback2(self,data):
        cloud_out = self.laserProj.projectLaser(data)
        position = point_cloud2.read_points(cloud_out, field_names=("y"))
        position_array = list(position)
        position_array = np.array(position_array)
        y_abs_sum = sum(abs(position_array))
        y_sum = sum(position_array) / y_abs_sum
        self.pcPub2.publish(cloud_out)
        self.sumPub2.publish(y_sum)
        
    def laserCallback3(self,data):
        cloud_out = self.laserProj.projectLaser(data)
        position = point_cloud2.read_points(cloud_out, field_names=("y"))
        position_array = list(position)
        position_array = np.array(position_array)
        y_abs_sum = sum(abs(position_array))
        y_sum = sum(position_array) / y_abs_sum
        self.pcPub3.publish(cloud_out)
        self.sumPub3.publish(y_sum)

    # def laserCallback4(self,data):
    #     cloud_out = self.laserProj.projectLaser(data)
    #     position = point_cloud2.read_points(cloud_out, field_names=("y"))
    #     position_array = list(position)
    #     position_array = np.array(position_array)
    #     y_abs_sum = sum(abs(position_array))
    #     y_sum = sum(position_array) / y_abs_sum
    #     self.pcPub4.publish(cloud_out)
    #     self.sumPub4.publish(y_sum)
        
    # def laserCallback5(self,data):
    #     cloud_out = self.laserProj.projectLaser(data)
    #     position = point_cloud2.read_points(cloud_out, field_names=("y"))
    #     position_array = list(position)
    #     position_array = np.array(position_array)
    #     y_abs_sum = sum(abs(position_array))
    #     y_sum = sum(position_array) / y_abs_sum
    #     self.pcPub5.publish(cloud_out)
    #     self.sumPub5.publish(y_sum)
        
    # def laserCallback6(self,data):
    #     cloud_out = self.laserProj.projectLaser(data)
    #     position = point_cloud2.read_points(cloud_out, field_names=("y"))
    #     position_array = list(position)
    #     position_array = np.array(position_array)
    #     y_abs_sum = sum(abs(position_array))
    #     y_sum = sum(position_array) / y_abs_sum
    #     self.pcPub6.publish(cloud_out)
    #     self.sumPub6.publish(y_sum)

if __name__ == '__main__':
    rospy.init_node("PointCloud")
    l2pc = Laser2PC2YSum()
    rospy.spin()