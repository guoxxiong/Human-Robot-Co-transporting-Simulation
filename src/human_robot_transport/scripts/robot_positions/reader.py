#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 12:35:01 2021

@author: guoxiong
"""


import csv


csvFile = open("robot1_xy.csv", "r")
reader = csv.reader(csvFile)


for item in reader:
    print(item[0])
    
csvFile.close()
