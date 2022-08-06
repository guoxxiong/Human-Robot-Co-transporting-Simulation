import rospy
import math
from sympy import *

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class Obstacle:
    LIDAR_ERROR = 0.05
    STOP_DISTANCE = 0.6
    SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR
    CONSTANT_DISTANCE = 1.0
    
    def __init__(self, trans):
        self.SD = Obstacle.SAFE_STOP_DISTANCE
        self.D = Obstacle.CONSTANT_DISTANCE
        self.x1 = trans[0]
        self.y1 = trans[1]
        (self.x2, self.y2) = self.convert_scan(Obstacle.get_scan())
        
        
    @staticmethod
    def get_scan():     
        scan = rospy.wait_for_message('/scan', LaserScan)       
        scan_filter = []
        samples = len(scan.ranges)
        scan_filter = list(scan.ranges)
        for i in range(samples):
            if scan_filter[i] == float('Inf'):
                scan_filter[i] = 10.0
            elif math.isnan(scan_filter[i]):
                scan_filter[i] = 0      
        return scan_filter
        
    @staticmethod
    def convert_scan(scan_filter):
        d = min(scan_filter)
        theta = (91 + scan_filter.index(min(scan_filter))) % 360 
        #(450 - (180 - (scan_filter.index(min(scan_filter)) - 179))) % 360
        x2 = d * math.cos(math.pi * round(theta / 180.0, 3))
        y2 = d * math.sin(math.pi * round(theta / 180.0, 3))
        return x2, y2
        
#    def inesc(self):
#        dr1r2 = round(math.sqrt(self.x1 ** 2 + self.y1 ** 2), 2)
#        dr = round(math.sqrt((abs(self.x2 - self.x1)) ** 2 + (abs(self.y2 - self.y1)) ** 2), 2)
#        Adr = round((dr1r2 ** 2 - self.SD ** 2 + dr ** 2) / (2 * dr), 2)
#        # print cls.D ** 2 - Adr ** 2
#        h = math.sqrt(round(dr1r2 ** 2 - Adr ** 2, 2))
#        cx = round(self.x1 + Adr * (self.x2 - self.x1) / dr, 2)
#        cy = round(self.y1 + Adr * (self.y2 - self.y1) / dr, 2)
#        x3 = round(cx - h * (self.y2 - self.y1) / dr, 2)
#        y3 = round(cy + h * (self.x2 - self.x1) / dr, 2)
#        x4 = round(cx + h * (self.y2 - self.y1) / dr, 2)
#        y4 = round(cy - h * (self.x2 - self.x1) / dr, 2)
#        if (x3 ** 2 + y3 ** 2) < (x4 ** 2 + y4 ** 2):
#            x = x3
#            y = y3
#        else:
#            x = x4
#            y = y4
#        return x, y
        
    def solve(self):
        x = Symbol('x')
        y = Symbol('y')
        solved_value = solve([(x - self.x1) ** 2 + (y - self.y1) ** 2 - self.D ** 2, (x - self.x2) ** 2 + (y - self.y2) ** 2 - self.SD ** 2])
        A1 = list(solved_value[0])
        A2 = list(solved_value[1])
        if (A1[0] ** 2 + A1[1] ** 2) < (A2[0] ** 2 + A2[1] ** 2):
            return A1[0], A1[1]
        else:
            return A2[0], A2[1]
        
#    def rotate(self):
#        twist = Twist()
#        if round(math.sqrt(self.x2 ** 2 + self.y2 ** 2), 2) < self.SD:
#            (X, Y) = self.solve()
#            if X < 0:
#                twist.linear.x = 0
#                twist.angular.z = 
#        else:
#            twist.linear.x = 0
#            twist.angular.z = 0
#        return twist
        
    def obstacle(self):
        twist = Twist()
        if round(math.sqrt(self.x2 ** 2 + self.y2 ** 2), 2) < self.SD:
#            (X, Y) = self.inesc()
            (X, Y) = self.solve()
            twist.linear.x = math.sqrt(X ** 2 + Y ** 2)
            twist.angular.z = math.atan2(0 - X, Y)  
        else:
            twist.linear.x = 0
            twist.angular.z = 0
        return twist
                


