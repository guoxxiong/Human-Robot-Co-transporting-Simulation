#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 22:17:22 2021

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
z_list = []
for item in reader:
    x_list.append(float(item[0]))
    y_list.append(float(item[1]))
    z_list.append(float(item[2]))

fig = plt.figure(figsize = (8, 4))
ax = fig.add_subplot(111)



#ax.set(xlim=[0, x_list[-1]], ylim=[1.19, 1.21], ylabel='distance[m]', xlabel='time[s]')
#ax.set(xlim=[0, x_list[-1]], ylim=[1.18, 1.22], ylabel='distance [m]', xlabel='time [s]')
ax.set(xlim=[0, x_list[-1]], ylim=[-0.6, 0.6], ylabel='speed [m/s]', xlabel='time [s]')

#desired_distance = np.ones(len(x_list)) * 1.2

ax.plot(x_list, y_list, color = "r", linewidth = 1.5)
ax.plot(x_list, z_list, color = "g", linewidth = 1.5)
ax.legend(labels = ["speed on x axis", "speed on y axis"])

plt.show()

