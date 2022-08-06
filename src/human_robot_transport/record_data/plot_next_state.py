#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 12:47:08 2021

@author: guoxiong
"""

import csv
from matplotlib import pyplot as plt
import matplotlib.patches as mpathes
import numpy as np

#csvFile = open("important_data/robot12_distance1625714794.csv", "r")
#csvFile = open("important_data/robot12_distance1625719960.csv", "r")
#csvFile = open("important_data/robot12_distance1625720419.csv", "r")
#csvFile = open("important_data/robot12_distance1625720613.csv", "r")
#csvFile = open("important_data/robot12_distance1625720990.csv", "r")
#csvFile = open("important_data/robot12_distance1625721128.csv", "r")
#csvFile = open("important_data2/robot_speed_and_distance05.csv", "r") 
csvFile = open("backward/next_state.csv", "r")
reader = csv.reader(csvFile)
csvFile1 = open("backward/robot2_odom.csv", "r")
reader1 = csv.reader(csvFile1)
csvFile2 = open("backward/cmd_vel_buf.csv", "r")
reader2 = csv.reader(csvFile2)
csvFile3 = open("backward/cmd_vel.csv", "r")
reader3 = csv.reader(csvFile3)

time_list = []
ex_list = []
ey_list = []
ew_list = []

time_list1 = []
actualvx = []
actualvy = []
actualwz = []

time_list2 = []
desiredvx = []
desiredvy = []
desiredwz = []

time_list3 = []
smoothvx = []
smoothvy = []
smoothwz = []

for item in reader:
    time_list.append(float(item[0]))
    ex_list.append(float(item[1]))
    ey_list.append(float(item[2]))
    ew_list.append(float(item[3]))

for item1 in reader1:
    time_list1.append(float(item1[0]))
    actualvx.append(float(item1[1]))
    actualvy.append(float(item1[2]))
    actualwz.append(float(item1[3]))

for item2 in reader2:
    time_list2.append(float(item2[0]))
    desiredvx.append(float(item2[1]))
    desiredvy.append(float(item2[2]))
    desiredwz.append(float(item2[3]))

for item3 in reader3:
    time_list3.append(float(item3[0]))
    smoothvx.append(float(item3[1]))
    smoothvy.append(float(item3[2]))
    smoothwz.append(float(item3[3]))

fig = plt.figure(figsize = (8, 4))
ax = fig.add_subplot(611)
aax = fig.add_subplot(612)
bx = fig.add_subplot(613)
bbx = fig.add_subplot(614)
cx = fig.add_subplot(615)
ccx = fig.add_subplot(616)

xy2 = np.array([0, 1.1])
rect = mpathes.Rectangle(xy2, 18, 0.2, color='b', alpha = 0.1)
ax.add_patch(rect)

#ax.set(xlim=[0, x_list[-1]], ylim=[1.19, 1.21], ylabel='distance[m]', xlabel='time[s]')
#ax.set(xlim=[0, x_list[-1]], ylim=[1.18, 1.22], ylabel='distance [m]', xlabel='time [s]')
ax.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.05, 0.1], ylabel='distance on X-axis [m]', xlabel='')
# aax.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.2, 0.7], ylabel='linear velocity on X-axis [m/s]', xlabel='')
aax.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.7, 0.4], ylabel='linear velocity on X-axis [m/s]', xlabel='')
bx.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.01, 0.01], ylabel='distance on Y-axis [m]', xlabel='')
bbx.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.5, 0.5], ylabel='linear velocity on Y-axis [m/s]', xlabel='')
# cx.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.03, 0.06], ylabel='angle on Z-axis [rad]', xlabel='')
cx.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.08, 0.06], ylabel='angle on Z-axis [rad]', xlabel='')
# ccx.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.45, 0.7], ylabel='angular velocity on Z-axis [rad/s]', xlabel='time [s]')
ccx.set(xlim=[time_list[0], time_list[-1]], ylim=[-0.8, 0.6], ylabel='angular velocity on Z-axis [rad/s]', xlabel='time [s]')


#desired_distance = np.ones(len(x_list)) * 1.2

x_max_distance = np.ones(len(time_list)) * max(ex_list)
y_max_distance = np.ones(len(time_list)) * max(ey_list)
max_angle = np.ones(len(time_list)) * max(ew_list)
x_min_distance = np.ones(len(time_list)) * min(ex_list)
y_min_distance = np.ones(len(time_list)) * min(ey_list)
min_angle = np.ones(len(time_list)) * min(ew_list)

ax.annotate(str(round(max(ex_list),3)), xy=(time_list[ex_list.index(max(ex_list))], max(ex_list)+0.006))
ax.annotate(str(round(min(ex_list),3)), xy=(time_list[ex_list.index(min(ex_list))]-5, min(ex_list)-0.016))
bx.annotate(str(round(max(ey_list),3)), xy=(time_list[ey_list.index(max(ey_list))], max(ey_list)+0.001))
bx.annotate(str(round(min(ey_list),3)), xy=(time_list[ey_list.index(min(ey_list))], min(ey_list)-0.002))
cx.annotate(str(round(max(ew_list),3)), xy=(time_list[ew_list.index(max(ew_list))], max(ew_list)+0.006))
cx.annotate(str(round(min(ew_list),3)), xy=(time_list[ew_list.index(min(ew_list))], min(ew_list)-0.010))

ax.plot(time_list, ex_list, color = "b", linewidth = 1.5)
ax.plot(time_list, x_min_distance, color = "c", linewidth = 2, linestyle = "--")
ax.plot(time_list, x_max_distance, color = "orange", linewidth = 2, linestyle = "--")

bx.plot(time_list, ey_list, color = "b", linewidth = 1.5)
bx.plot(time_list, y_min_distance, color = "c", linewidth = 2, linestyle = "--")
bx.plot(time_list, y_max_distance, color = "orange", linewidth = 2, linestyle = "--")

cx.plot(time_list, ew_list, color = "b", linewidth = 1.5)
cx.plot(time_list, min_angle, color = "c", linewidth = 2, linestyle = "--")
cx.plot(time_list, max_angle, color = "orange", linewidth = 2, linestyle = "--")

#plt.plot(desired_distance, color = "r", linewidth =2, linestyle = "--")
ax.legend(ncol = 3, labels = ["actual",  "minimum", "maximum"], loc = 1)
bx.legend(ncol = 3, labels = ["actual",  "minimum", "maximum"], loc = 1)
cx.legend(ncol = 3, labels = ["actual",  "minimum", "maximum"], loc = 1)

aax.plot(time_list1, actualvx, color = 'b', linewidth = 1.5)
aax.plot(time_list2, desiredvx  - np.ones(len(time_list2)) * 0.05, color = 'r', linewidth = 1)
aax.plot(time_list3, smoothvx  - np.ones(len(time_list3)) * 0.1, color = 'c', linewidth = 1)

bbx.plot(time_list1, actualvy, color = 'b', linewidth = 1.5)
bbx.plot(time_list2, desiredvy - np.ones(len(time_list2)) * 0.05, color = 'r', linewidth = 1)
bbx.plot(time_list3, smoothvy - np.ones(len(time_list3)) * 0.1, color = 'c', linewidth = 1)

ccx.plot(time_list1, actualwz, color = 'b', linewidth = 1.5)
ccx.plot(time_list2, desiredwz - np.ones(len(time_list2)) * 0.05, color = 'r', linewidth = 1)
ccx.plot(time_list3, smoothwz - np.ones(len(time_list3)) * 0.1, color = 'c', linewidth = 1)

aax.legend(ncol = 3, labels = ["actual",  "desired - 0.05", "smoothed - 0.1"], loc = 1)
bbx.legend(ncol = 3, labels = ["actual",  "desired - 0.05", "smoothed - 0.1"], loc = 1)
ccx.legend(ncol = 3, labels = ["actual",  "desired - 0.05", "smoothed - 0.1"], loc = 1)



plt.show()

