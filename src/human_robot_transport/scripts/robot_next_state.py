#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2021.11.28

@author: guoxiong
"""

import rospy
import math
import numpy as np
from scipy.spatial.transform import Rotation as R
from gazebo_msgs.msg import LinkStates
from human_robot_transport.msg import NextPose
from parameters import b1, b2
from rospy.core import rospyinfo


topic = "/gazebo/link_states"


class robotNextState():

    def __init__(self, topic_name):
        self.topicName = topic_name
        self.lss = self.get_link_states()

    def get_link_states(self):
        '''
        Obtain link states from gazebo.
        input: topicName (string)
        output: states (gazebo_msgs/LinkStates)
        '''
        link_states = rospy.wait_for_message(self.topicName, LinkStates)
        return link_states


    @staticmethod
    def quaternion2euler(quaternion):
        '''
        Convert quaternion to euler.
        input: Gazebo/LinkStates.pose.orientation (quaternion)
        output: yaw, pitch, roll (euler)
        '''
        r = R.from_quat(quaternion)
        euler = r.as_euler('zyx', degrees=False)
        # print(euler[0])
        return euler

    @staticmethod
    def judge_d_sign(x_cs, y_cs, theta_cs):
        '''
        Determine the sign of d.
        input: The coordinates and orientation of the slider relative to the disc (float64)
        output: +1 or -1 (int)
        '''
        need_process_flag = False
        angle_jump_thresh = {"min": -0.001, "max": 0.001}

        # if (theta_cs < angle_jump_thresh["min"]):
        #     need_process_flag = True
        #     theta_cs = theta_cs + 2*math.pi
        #     if ((x_cs > 0) and (y_cs > 0) and (theta_cs > 0) and (theta_cs < 0.5*math.pi)) or \
        #         ((x_cs > 0) and (y_cs < 0) and (theta_cs > 1.5*math.pi) and (theta_cs < 2*math.pi)) or \
        #             ((x_cs > 0) and (y_cs == 0) and (theta_cs == 0)) or \
        #                 ((x_cs == 0) and (y_cs > 0) and (theta_cs == 0.5*math.pi)) or \
        #                     ((x_cs == 0) and (y_cs < 0) and (theta_cs == 1.5*math.pi)) or \
        #                         ((x_cs < 0) and (y_cs > 0) and (theta_cs > 0.5*math.pi) and (theta_cs < math.pi)) or \
        #                             ((x_cs < 0) and (y_cs == 0) and (theta_cs == math.pi)) or \
        #                                 ((x_cs < 0) and (y_cs < 0) and (theta_cs > math.pi) and (theta_cs < 1.5*math.pi)) :
        #                                 return need_process_flag, 1
        #     else:
        #         return need_process_flag, -1 
        #     pass

        # elif (theta_cs > angle_jump_thresh["max"]):
        #     need_process_flag = True
        #     if ((x_cs > 0) and (y_cs > 0) and (theta_cs > 0) and (theta_cs < 0.5*math.pi)) or \
        #         ((x_cs > 0) and (y_cs < 0) and (theta_cs > 1.5*math.pi) and (theta_cs < 2*math.pi)) or \
        #             ((x_cs > 0) and (y_cs == 0) and (theta_cs == 0)) or \
        #                 ((x_cs == 0) and (y_cs > 0) and (theta_cs == 0.5*math.pi)) or \
        #                     ((x_cs == 0) and (y_cs < 0) and (theta_cs == 1.5*math.pi)) or \
        #                         ((x_cs < 0) and (y_cs > 0) and (theta_cs > 0.5*math.pi) and (theta_cs < math.pi)) or \
        #                             ((x_cs < 0) and (y_cs == 0) and (theta_cs == math.pi)) or \
        #                                 ((x_cs < 0) and (y_cs < 0) and (theta_cs > math.pi) and (theta_cs < 1.5*math.pi)) :
        #                                 return need_process_flag, 1
        #     else:
        #         return need_process_flag, -1
        #     pass

        if (theta_cs < angle_jump_thresh["min"]):
            need_process_flag = True
            if ((x_cs > 0) and (y_cs < 0)) or \
                ((x_cs < 0) and (y_cs > 0)):
                return need_process_flag, 1
            else:
                need_process_flag = False
                return need_process_flag, -1 
            pass

        elif (theta_cs > angle_jump_thresh["max"]):
            need_process_flag = True
            if ((x_cs > 0) and (y_cs > 0)) or \
                ((x_cs < 0) and (y_cs < 0)):
                return need_process_flag, 1
            else:
                need_process_flag = False
                return need_process_flag, -1
            pass

        elif ((theta_cs > angle_jump_thresh["min"]) or (theta_cs == angle_jump_thresh["min"])) and ((theta_cs < angle_jump_thresh["max"]) or (theta_cs == angle_jump_thresh["max"])):
            need_process_flag = False
            return need_process_flag, 0
            pass

    def cal_d_theta(self):
        '''
        Calculate the relative pose between disc and slider.
        input: Gazebo/LinkStates (gazebo_msgs)
        output: d, theta (float64)
        '''
        discxyz = self.lss.pose[list(self.lss.name).index("robot2::Link3")].position
        discxyzw = self.lss.pose[list(self.lss.name).index("robot2::base_footprint")].orientation
        sliderxyz = self.lss.pose[list(self.lss.name).index("robot2::Link4Slider")].position
        sliderxyzw = self.lss.pose[list(self.lss.name).index("robot2::Link4Slider")].orientation
        woodxyz = self.lss.pose[list(self.lss.name).index("wood::base_footprint")].position
        d_x = sliderxyz.x - discxyz.x
        d_y = sliderxyz.y - discxyz.y
        d_z = woodxyz.z - sliderxyz.z
        d = math.sqrt(d_x * d_x + d_y * d_y)
        disc_quat = np.array([discxyzw.x, discxyzw.y, discxyzw.z, discxyzw.w])
        slider_quat = np.array([sliderxyzw.x, sliderxyzw.y, sliderxyzw.z, sliderxyzw.w])
        disc_eul = self.quaternion2euler(disc_quat)
        slider_eul = self.quaternion2euler(slider_quat)
        if (disc_eul[0] < 0) or (disc_eul[0] == 0):
            yaw1 = 2 * math.pi + disc_eul[0]
        elif disc_eul[0] > 0:
            yaw1 = disc_eul[0]
        if (slider_eul[0] < 0) or (slider_eul[0] == 0):
            yaw2 = 2 * math.pi + slider_eul[0]
        elif slider_eul[0] > 0:
            yaw2 = slider_eul[0]
        if yaw2 - yaw1 < 0.5 - 2 * math.pi: #yaw2 - yaw1 < -2*math.pi + 0.1
            theta = yaw2 - yaw1 + 2 * math.pi
        elif yaw2 - yaw1 > 2 * math.pi - 0.5:
            theta = yaw2 - yaw1 - 2 * math.pi
        else:
            theta = yaw2 - yaw1
        # flag, PN = self.judge_d_sign(d_x, d_y, theta)
        #Waiting for slider fixed to slider
        # if (d_z < 0.04) and (d_z > 0.02)
        #     if flag == True:
        #         d = d * PN
        #     else:
        #         d = d_x
        # else:
        #     d = d_x
        print("-------------------------------------------------")
        print(d)
        print(theta)
        return d, theta
        
    @staticmethod
    def mechanism_converse(hat_d, hat_theta):
        '''
        Calculate the next pose of the slider with mechanism constrains.
        input: hat_d, hat_theta (float64)
        output: a state vector (human_robot_transport.msg/NextPose)
        '''
        slider_next_state = NextPose()
        slider_next_state.x = (hat_d - b1 - b2) * math.cos(hat_theta) + b1
        slider_next_state.y = (hat_d - b1 - b2) * math.sin(hat_theta)
        slider_next_state.theta = hat_theta
        return slider_next_state


if __name__ == "__main__":
    rospy.init_node("robot_next_state")
    rate = rospy.Rate(200.0)
    pub = rospy.Publisher("robot2NextState", NextPose, queue_size=1)
    while not rospy.is_shutdown():
        rns = robotNextState(topic)
        dd, ttheta = rns.cal_d_theta()
        goal_state = rns.mechanism_converse(dd, ttheta)
        pub.publish(goal_state)
        # rospy.loginfo("[Parse State]::: " + str(goal_state))
        rate.sleep()

