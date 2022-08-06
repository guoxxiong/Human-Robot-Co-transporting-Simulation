#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 13:18:35 2021

@author: guoxiong
"""


import numpy as np
from matplotlib import pyplot as plt

x_point = [5.51, 5.42, 3.49, 2.04]
y_point = [-2.53, -5.48, -3.47, -2.36]
l1 = np.linspace(0, 8, 10)
l2 = np.zeros(10)
l3 = np.ones(10) * 8
l4 = np.linspace(-8, 0, 10)
l41 = np.linspace(0, 1.9, 10)
l42 = np.linspace(3.1, 8, 10)
l5 = np.ones(10) * (-8)
l6 = np.linspace(-2, 0, 10)
l7 = np.linspace(-5, -3.2, 10)
l8 = np.linspace(-8, -6.1, 10)




plt.figure(figsize = (10, 10))
plt.scatter(x_point, y_point, s = 100, c = "r", linewidth = 30)
plt.annotate('obstacle1', xy=(5.51,-2.53), xytext=(5.8,-2.3)) 
plt.annotate('obstacle2', xy=(5.42,-5.48), xytext=(5.8,-5.3))
plt.annotate('obstacle3', xy=(3.49,-3.47), xytext=(3.2,-4)) 
plt.annotate('obstacle4', xy=(2.04,-2.36), xytext=(2,-2))
plt.annotate('wall', c = 'w', fontsize = 15, xy=(0.5, -0.1))
#plt.plot(l1, l2, c = "r", linewidth = 20)
plt.plot(l1, l5, c = "r", linewidth = 20)
plt.plot(l2, l4, c = "r", linewidth = 20)
plt.plot(l41, l2, c = "r", linewidth = 20)
plt.plot(l42, l2, c = "r", linewidth = 20)
plt.plot(l3, l6, c = "r", linewidth = 20)
plt.plot(l3, l7, c = "r", linewidth = 20)
plt.plot(l3, l8, c = "r", linewidth = 20)
plt.xlabel('x[m]', color='#1C2833')
plt.ylabel('y[m]', color='#1C2833')
plt.xlim(-0.5, 8.5)
plt.ylim(-8.5, 0.5)

plt.grid(False)
plt.show()