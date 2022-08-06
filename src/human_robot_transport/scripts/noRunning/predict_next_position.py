#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 17:04:17 2021

@author: guoxiong
"""

import threading
import numpy as np
import rospy
import tf
from human_robot_transport.msg import Position
from human_robot_transport.msg import Positions

N = 5

def position_process():
    listener = tf.TransformListener()
    positions_pub = rospy.Publisher("human_position", Positions, queue_size = 1)
    positions = Positions()
    rate = rospy.Rate(100.0)
    Xposition = np.zeros(5)
    Yposition = np.zeros(5)
    i = 0
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform('/robot2/odom', '/robot1/odom', rospy.Time())
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        if i < N:
            Xposition[i] = trans[0]
            Yposition[i] = trans[1]
            i = i + 1
        else:
            positions.X = Xposition
            positions.Y = Yposition
            positions_pub.publish(positions)
            Xposition[:-1] = Xposition[1:]
            Xposition[i-1] = trans[0]
            Yposition[:-1] = Yposition[1:]
            Yposition[i-1] = trans[1]
        rate.sleep()

def parameter_estimation_and_predict(T, X, Y):
    n = len(T)
    Xdinominator = 0
    Xnumerator = 0
    Ydinominator = 0
    Ynumerator = 0
    for i in range(0, n):
        Xnumerator += (T[i] - np.mean(T)) * X[i]
        Ynumerator += (T[i] - np.mean(T)) * Y[i]
        Xdinominator +=  T[i] ** 2 - T[i] * np.mean(T)
        Ydinominator += T[i] ** 2 - T[i] * np.mean(T)
    Wx = Xnumerator / float(Xdinominator)
    Wy = Ynumerator / float(Ydinominator)
    bx = np.mean(X) - Wx * np.mean(T)
    by = np.mean(Y) - Wy * np.mean(T)
    return Wx * 6 + bx, Wy * 6 + by

def predict_pub():
    rate = rospy.Rate(100.0)
    position_pub = rospy.Publisher("predicted_position", Position, queue_size = 1)
    position = Position()
    Time = [1, 2, 3, 4, 5]
    while not rospy.is_shutdown():
        P = rospy.wait_for_message("human_position", Positions)
        position.x, position.y = parameter_estimation_and_predict(Time, P.X, P.Y)
        position_pub.publish(position)
        rate.sleep()
        
if __name__ == "__main__":
    rospy.init_node("predict_next_position")
    th1 = threading.Thread(target = position_process)
    th2 = threading.Thread(target = predict_pub)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    rospy.spin()
    