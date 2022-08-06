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
csvFile = open("robot_speed_and_distance1627918447.csv", "r")
reader = csv.reader(csvFile)

x_list = []
y_list = []
for item in reader:
    x_list.append(float(item[0]))
    y_list.append(float(item[3]))

fig = plt.figure(figsize = (8, 4))
ax = fig.add_subplot(111)

xy2 = np.array([0, 1.1])
rect = mpathes.Rectangle(xy2, 18, 0.2, color='b', alpha = 0.1)
ax.add_patch(rect)

#ax.set(xlim=[0, x_list[-1]], ylim=[1.19, 1.21], ylabel='distance[m]', xlabel='time[s]')
#ax.set(xlim=[0, x_list[-1]], ylim=[1.18, 1.22], ylabel='distance [m]', xlabel='time [s]')
ax.set(xlim=[0, x_list[-1]], ylim=[1.08, 1.34], ylabel='distance [m]', xlabel='time [s]')

#desired_distance = np.ones(len(x_list)) * 1.2
desired_distance = np.ones(len(x_list)) *1.2
max_distance = np.ones(len(x_list)) * max(y_list)
plt.annotate(str(max(y_list)), xy=(x_list[y_list.index(max(y_list))], max(y_list)+0.006))
min_distance = np.ones(len(x_list)) * min(y_list)
plt.annotate(str(min(y_list)), xy=(x_list[y_list.index(min(y_list))], min(y_list)-0.016))
ax.plot(x_list, y_list, color = "b", linewidth = 1.5)
ax.plot(x_list, desired_distance, color = "r", linewidth = 2, linestyle = "--")
ax.plot(x_list, min_distance, color = "c", linewidth = 2, linestyle = "--")
ax.plot(x_list, max_distance, color = "orange", linewidth = 2, linestyle = "--")
#plt.plot(desired_distance, color = "r", linewidth =2, linestyle = "--")
ax.legend(ncol = 4, labels = ["actual", "object length", "minimum", "maximum"], loc = 2)



plt.show()

