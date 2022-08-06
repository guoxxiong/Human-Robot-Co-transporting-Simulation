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

csvFile = open("robot_speed_and_distance1628003113.csv", "r")

reader = csv.reader(csvFile)

x_list = []
y_list = []
z_list = []
for item in reader:
    x_list.append(float(item[0]))
    y_list.append(float(item[1]))
    z_list.append(float(item[3]))

fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(211)
bx = fig.add_subplot(212)

xy2 = np.array([0, 1.1])
rect = mpathes.Rectangle(xy2, 8, 0.2, color='b', alpha = 0.1)
bx.add_patch(rect)

#ax.set(xlim=[0, x_list[-1]], ylim=[1.19, 1.21], ylabel='distance[m]', xlabel='time[s]')
#ax.set(xlim=[0, x_list[-1]], ylim=[1.18, 1.22], ylabel='distance[m]', xlabel='time[s]')
ax.set(xlim=[0, x_list[-1]], ylim=[-1, 1], ylabel='human velocity [m/s]')
bx.set(xlim=[0, x_list[-1]], ylim=[1.02, 1.32], ylabel='distance [m]', xlabel='time [s]')

desired_distance = np.ones(len(x_list)) * 1.2
#desired_distance = np.ones(len(x_list)) * 0.6

max_distance = np.ones(len(x_list)) * max(z_list)
bx.annotate(str(max(z_list)), xy=(x_list[z_list.index(max(z_list))], max(z_list)+0.003))
min_distance = np.ones(len(x_list)) * min(z_list)
bx.annotate(str(min(z_list)), xy=(x_list[z_list.index(min(z_list))]-0.3, min(z_list)+0.015))
bx.plot(x_list, z_list, color = "b", linewidth = 1)
bx.plot(x_list, desired_distance, color = "r", linewidth = 2, linestyle = "--")
bx.plot(x_list, min_distance, color = "c", linewidth = 2, linestyle = "--")
bx.plot(x_list, max_distance, color = "orange", linewidth = 2, linestyle = "--")
#plt.plot(desired_distance, color = "r", linewidth =2, linestyle = "--")
bx.legend(ncol = 4, labels = ["actual", "object length", "minimum", "maximum"], loc = 3)

ax.plot(x_list, y_list, color = "lime", linewidth = 1)
ax.annotate(str(max(y_list)), xy=(x_list[y_list.index(max(y_list))]-0.03, max(y_list)+0.1))
ax.annotate(str(min(y_list)), xy=(x_list[y_list.index(min(y_list))]-0.03, min(y_list)-0.3))
plt.show()

