#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 20:33:37 2021

@author: guoxiong
"""


import numpy as np
from matplotlib import pyplot as plt
import csv

csvFile1 = open("SCE1/hand_pos.csv", "r")
csvFile2 = open("SCE1/slider_pos.csv", "r")
csvFile3 = open("SCE1/robot_pos.csv", "r")
reader1 = csv.reader(csvFile1)
reader2 = csv.reader(csvFile2)
reader3 = csv.reader(csvFile3)


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
l9 = np.linspace(-2, 0, 10)

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
plt.plot(l2, l9, c = "orange", linewidth = 20)
plt.plot(l3, l9, c = "orange", linewidth = 20)
plt.xlabel('x [m]', color='#1C2833')
plt.ylabel('y [m]', color='#1C2833')
plt.xlim(-4.1, 8.5)
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
plt.scatter(robot1_x, robot1_y, s = 10, c = "b", linewidth = 0.5, label = "human hand trajectory")

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
    
robotx = []
roboty = []
count3 = 0 
for item3 in reader3:
    if count3 % 50 == 0:
        count3 = 0
        robotx.append(round(float(item3[0]), 4))
        roboty.append(round(float(item3[1]), 4))
    count3 = count3 + 1
    

    
plt.scatter(robot2_x, robot2_y, s = 10, c = "r", linewidth = 0.5, label = "slider trajectory")



#sample_x1.append(5.071)
#sample_x2.append(5.150)
#sample_y1.append(6.560)
#sample_y2.append(5.321)

for i in range(0, len(sample_x1)):
    x1 = sample_x1[i]
    x2 = sample_x2[i]
    y1 = sample_y1[i]
    y2 = sample_y2[i]
    plt.plot([x1 + 0.16 * (x2 - x1), x2 - 0.16 * (x2 - x1)], [y1 + 0.16 * (y2 - y1), y2 - 0.16 * (y2 - y1)], c = "c", linewidth = 20, alpha = 0.2)
    plt.plot([sample_x1[i], sample_x2[i]], [sample_y1[i], sample_y2[i]], c = "c", linewidth = 1, alpha = 0.8)

# means
rtx = [-3.85, -0.3, -0.3, -3.85, -3.85]
rty = [-0.3, -0.3, -2.4, -2.4, -0.3]
plt.plot(rtx, rty, c = "gray", alpha = 0.5)
plt.plot([-3.5,-2.5], [-0.6,-0.6], c = "c", linewidth = 20, alpha = 0.2)
plt.annotate('board', xy=(-2.1, -0.65))
plt.plot([-3.65,-2.35], [-0.6,-0.6], c = "c", linewidth = 1, alpha = 0.8)
plt.plot([-3.5,-2.5], [-1.1,-1.1], c = "orange", linewidth = 20)
plt.annotate('wall', xy=(-2.1, -1.15))
plt.plot([-3.65,-2.8], [-1.5,-1.5], c = "b", linewidth = 5)
plt.annotate('human hand trajectory', xy=(-2.6, -1.55))
plt.plot([-3.65,-2.8], [-1.8,-1.8], c = "r", linewidth = 5)
plt.annotate('slider trajectory', xy=(-2.6, -1.85))
plt.scatter(-3.4, -2.15, s = 20, c = "k", linewidth = 1)
plt.annotate('robot geometric center', xy=(-2.8, -2.2))

plt.scatter(robotx, roboty, s = 20, c = "k", linewidth = 1, label = "robot point")


plt.grid(False)
plt.show()
