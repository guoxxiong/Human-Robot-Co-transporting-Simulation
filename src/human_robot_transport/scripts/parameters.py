#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 20:57:15 2021

@author: guoxiong
"""


D = 1.105
#OFFSET_FACTOR = 0.5
C1_WEIGHT = 0.1
C2_WEIGHT = 0.25
C3_WEIGHT = 0.65

# 1 / (2*math.pi*D), D = 1.2
W_v_1 = 0.132629

# D = 0.6
# W_v_1 = 0.265258

#derive next state of the robot
b1 = 0.10525
b2 = 0.02

