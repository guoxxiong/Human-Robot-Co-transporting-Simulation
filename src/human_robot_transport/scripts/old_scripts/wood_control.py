import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

def wood_control():
    pub = rospy.Publisher("wood/cmd_vel", Twist, queue_size = 1)
    rate = rospy.Rate(20.0)
    while not rospy.is_shutdown():
        twist = Twist()
        data1 = rospy.wait_for_message("robot1/odom", Odometry, timeout = 5)
        data2 = rospy.wait_for_message("robot2/odom", Odometry, timeout = 5)
        data3 = rospy.wait_for_message("wood/odom", Odometry, timeout = 5)
        x1 = data1.pose.pose.position.x
        y1 = data1.pose.pose.position.y
        x2 = data2.pose.pose.position.x
        y2 = data2.pose.pose.position.y
        x3 = data3.pose.pose.position.x
        y3 = data3.pose.pose.position.y
        x4 = (x1 + x2) / 2
        y4 = (y1 + y2) / 2
        twist.linear.x = math.sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = - math.atan2(x1 - x2, y1 - y2)
        print(twist)
        pub.publish(twist)
        rate.sleep()
        
if __name__ == "__main__":
    rospy.init_node("wood_control")
    wood_control()