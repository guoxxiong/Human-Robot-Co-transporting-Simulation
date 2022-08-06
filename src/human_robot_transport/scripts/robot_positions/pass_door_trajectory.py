#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 20:33:37 2021

@author: guoxiong
"""


import numpy as np
from matplotlib import pyplot as plt
import csv

csvFile1 = open("hand_pos.csv", "r")
csvFile2 = open("slider_pos.csv", "r")
reader1 = csv.reader(csvFile1)
reader2 = csv.reader(csvFile2)


x_point = [5.51, 5.42, 3.49, 2.04]
y_point = [-2.53, -5.48, -3.47, -2.36]
l1 = np.linspace(0, 8, 10)
l2 = np.zeros(10)
l3 = np.ones(10) * 8
l4 = np.linspace(0, 8, 10)
l41 = np.linspace(6.1, 8, 10)
l42 = np.linspace(0, 4.9, 10)
l5 = np.ones(10) * (8)
l6 = np.linspace(0, 2.1, 10)
l7 = np.linspace(3.2, 4.9, 10)
l8 = np.linspace(6.1, 8, 10)

# obstacle_scene
plt.figure(figsize = (12, 11.1))
#plt.scatter(x_point, y_point, s = 100, c = "orange", linewidth = 30)
#plt.annotate('obstacle1', xy=(5.51,-2.53), xytext=(5.8,-2.3)) 
#plt.annotate('obstacle2', xy=(5.42,-5.48), xytext=(5.8,-5.3))
#plt.annotate('obstacle3', xy=(3.49,-3.47), xytext=(3.2,-4)) 
#plt.annotate('obstacle4', xy=(2.04,-2.36), xytext=(2,-2))
#plt.annotate('wall', c = 'w', fontsize = 15, xy=(0.5, -0.1))
#plt.plot(l1, l2, c = "r", linewidth = 20)
plt.plot(l1, l5, c = "orange", linewidth = 20)
plt.plot(l3, l4, c = "orange", linewidth = 20)
plt.plot(l2, l41, c = "orange", linewidth = 20)
plt.plot(l2, l42, c = "orange", linewidth = 20)
plt.plot(l6, l2, c = "orange", linewidth = 20)
plt.plot(l7, l2, c = "orange", linewidth = 20)
plt.plot(l8, l2, c = "orange", linewidth = 20)
plt.xlabel('x [m]', color='#1C2833')
plt.ylabel('y [m]', color='#1C2833')
plt.xlim(-4, 8.5)
plt.ylim(-2.6, 8.5)

#robot_trajectory
robot1_x = []
robot1_y = []
sample_x1 = []
sample_y1 = []
count1 = 0


for item1 in reader1:
    robot1_x.append(round(float(item1[0]), 4))
    robot1_y.append(round(float(item1[1]), 4))
    if count1 % 50 == 0:
        count1 = 0
        sample_x1.append(round(float(item1[0]), 4))
        sample_y1.append(round(float(item1[1]), 4))
    count1 = count1 + 1
plt.scatter(robot1_x, robot1_y, s = 10, c = "b", linewidth = 0.5, label = "human trajectory")

robot2_x = []
robot2_y = []
sample_x2 = []
sample_y2 = []
count2 = 0

for item2 in reader2:
    robot2_x.append(round(float(item2[0]), 4))
    robot2_y.append(round(float(item2[1]), 4))
    if count2 % 50 == 0:
        count2 = 0
        sample_x2.append(round(float(item2[0]), 4))
        sample_y2.append(round(float(item2[1]), 4))
    count2 = count2 + 1
    
plt.scatter(robot2_x, robot2_y, s = 10, c = "r", linewidth = 0.5, label = "robot trajectory")

#sample_x1.append(5.071)
#sample_x2.append(5.150)
#sample_y1.append(6.560)
#sample_y2.append(5.321)

for i in range(0, len(sample_x1)):
    x1 = sample_x1[i]
    x2 = sample_x2[i]
    y1 = sample_y1[i]
    y2 = sample_y2[i]
    plt.plot([x1 + 0.16 * (x2 - x1), x2 - 0.16 * (x2 - x1)], [y1 + 0.16 * (y2 - y1), y2 - 0.16 * (y2 - y1)], c = "c", linewidth = 30, alpha = 0.2)
    plt.plot([sample_x1[i], sample_x2[i]], [sample_y1[i], sample_y2[i]], c = "c", linewidth = 1, alpha = 0.8)

# means
rtx = [-3.85, 0, 0, -3.85, -3.85]
rty = [-0.4, -0.4, -2.4, -2.4, -0.4]
plt.plot(rtx, rty, c = "gray", alpha = 0.5)
plt.plot([-3.4,-2.5], [-0.8,-0.8], c = "c", linewidth = 30, alpha = 0.2)
plt.annotate('object', xy=(-2, -0.85))
plt.plot([-3.55,-2.35], [-0.8,-0.8], c = "c", linewidth = 1, alpha = 0.8)
plt.plot([-3.5,-2.5], [-1.4,-1.4], c = "orange", linewidth = 20)
plt.annotate('wall', xy=(-2.1, -1.45))
plt.plot([-3.65,-2.5], [-1.8,-1.8], c = "b", linewidth = 5)
plt.annotate('human trajectory', xy=(-2.2, -1.85))
plt.plot([-3.65,-2.5], [-2.2,-2.2], c = "r", linewidth = 5)
plt.annotate('robot trajectory', xy=(-2.2, -2.25))


plt.grid(False)
plt.show()
