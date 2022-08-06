#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 22:57:23 2021

@author: guoxiong
"""


import csv
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.patches as mpathes

csvFile = open("robot_speed_and_distance1628054481.csv", "r")

reader = csv.reader(csvFile)

n_list = []
x_list = []
y_list = []
w_list = []
d_list = []
for item in reader:
    n_list.append(float(item[0]))
    x_list.append(float(item[1]))
    y_list.append(float(item[2]))
    w_list.append(float(item[3]))
    d_list.append(float(item[4]))

fig = plt.figure(figsize = (8, 9))
ax = fig.add_subplot(311)
bx = fig.add_subplot(312)
cx = fig.add_subplot(313)

#ax.set(xlim=[0, x_list[-1]], ylim=[1.19, 1.21], ylabel='distance[m]', xlabel='time[s]')
#ax.set(xlim=[0, x_list[-1]], ylim=[1.18, 1.22], ylabel='distance[m]', xlabel='time[s]')
ax.set(xlim=[0, n_list[-1]], ylim=[1.04, 1.32], ylabel='distance [m]')
bx.set(xlim=[0, n_list[-1]], ylim=[-0.6, 0.7], ylabel='robot linear velocity [m/s]')
cx.set(xlim=[0, n_list[-1]], ylim=[-0.6, 0.6], ylabel='robot angular velocity [rad/s]', xlabel='time [s]')

desired_distance = np.ones(len(n_list)) * 1.2
#desired_distance = np.ones(len(n_list)) * 0.6

xy2 = np.array([0, 1.1])
rect = mpathes.Rectangle(xy2, 35, 0.2, color='b', alpha = 0.1)
ax.add_patch(rect)

max_distance = np.ones(len(n_list)) * max(d_list)
ax.annotate(str(max(d_list)), xy=(n_list[d_list.index(max(d_list))], max(d_list)+0.003))
min_distance = np.ones(len(n_list)) * min(d_list)
ax.annotate(str(min(d_list)), xy=(n_list[d_list.index(min(d_list))]-0.3, min(d_list)+0.015))
ax.plot(n_list, desired_distance, color = "r", linewidth = 2, linestyle = "--")
#ax.plot(n_list, min_distance, color = "c", linewidth = 2, linestyle = "--")
ax.plot(n_list, max_distance, color = "orange", linewidth = 2, linestyle = "--")
ax.plot(n_list, d_list, color = "b", linewidth = 1.5)
ax.legend(ncol = 4, labels = ["object length", "maximum", "actual"], loc = 3)

bx.plot(n_list, x_list, color = "r", linewidth = 1)
bx.plot(n_list, y_list, color = "lime", linewidth = 1)
bx.annotate(str(max(x_list)), xy=(n_list[x_list.index(max(x_list))]-0.3, max(x_list)+0.015))
bx.annotate(str(max(y_list)), xy=(n_list[y_list.index(max(y_list))]-0.3, max(y_list)+0.015))
bx.annotate(str(min(y_list)), xy=(n_list[y_list.index(min(y_list))]-0.3, min(y_list)-0.1))
bx.legend(labels = ["velocity on x axis", "velocity on y axis"])


cx.plot(n_list, w_list, color = "c", linewidth = 1)
cx.annotate(str(max(w_list)), xy=(n_list[w_list.index(max(w_list))]-0.3, max(w_list)+0.015))
cx.annotate(str(min(w_list)), xy=(n_list[w_list.index(min(w_list))]-0.3, min(w_list)-0.1))
#plt.plot(desired_distance, color = "r", linewidth =2, linestyle = "--")



#bx.annotate(str(max(n_list)), xy=(x_list[y_list.index(max(y_list))]-0.03, max(y_list)+0.1))
#bx.annotate(str(min(n_list)), xy=(x_list[y_list.index(min(y_list))]-0.03, min(y_list)-0.3))
plt.show()

