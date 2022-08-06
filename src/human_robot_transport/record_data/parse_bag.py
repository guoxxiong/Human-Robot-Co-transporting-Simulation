import rosbag
from gazebo_msgs.msg import LinkStates
from geometry_msgs.msg import Twist
from human_robot_transport.msg import Motion
from human_robot_transport.msg import NextPose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import csv

LS = False
TW = True
MO = False
NP = False
OO = False
IMU = False

#loading the bag file
bag_file = 'backward.bag'
out_dir = bag_file[:-4] + "/"
bag = rosbag.Bag(bag_file, "r")

def LS_parse(flag):
    if flag == True:
        
        bag_data = bag.read_messages("/gazebo/link_states")
        msg_count = 0
        f1 = open(out_dir + "hand_pos.csv", 'w')
        writer1 = csv.writer(f1)
        f2 = open(out_dir + "slider_pos.csv", 'w')
        writer2 = csv.writer(f2)
        f3 = open(out_dir + "robot_pos.csv", 'w')
        writer3 = csv.writer(f3)

        for topic, msg, t in bag_data:
            msg_count = msg_count + 1
            if msg_count % 50 == 0:
                hpxy = []
                sdxy = []
                rxy = []
                hand_pos = msg.pose[list(msg.name).index("robot1::Link3")].position
                print(msg_count)
                print(hand_pos)
                hpxy.append(hand_pos.x)
                hpxy.append(hand_pos.y)
                writer1.writerow(hpxy)
                
                slider_pos = msg.pose[list(msg.name).index("robot2::Link4Slider")].position
                sdxy.append(slider_pos.x)
                sdxy.append(slider_pos.y)
                writer2.writerow(sdxy)

                robot_pos = msg.pose[list(msg.name).index("robot2::base_footprint")].position
                rxy.append(robot_pos.x)
                rxy.append(robot_pos.y)
                writer3.writerow(rxy)
    else:
        pass

def TW_parse(flag):
    if flag == True:
        
        bag_data1 = bag.read_messages("/robot2/cmd_vel")
        bag_data2 = bag.read_messages("/robot2/cmd_vel_buf")
        msg_count = 0
        f1 = open(out_dir + "cmd_vel.csv", 'w')
        writer1 = csv.writer(f1)
        f2 = open(out_dir + "cmd_vel_buf.csv", 'w')
        writer2 = csv.writer(f2)

        for topic, msg, t in bag_data1:
            msg_count = msg_count + 1
            if msg_count % 1 == 0:
                velxyw = []
                vx = msg.linear.x
                vy = msg.linear.y
                wz = msg.angular.z
                print(t)
                velxyw.append(int(str(t))*0.000000001)
                velxyw.append(vx)
                velxyw.append(vy)
                velxyw.append(wz)
                if (not vx == None) and (not vy == None):
                    writer1.writerow(velxyw)

        for topic, msg, t in bag_data2:
            msg_count = msg_count + 1
            if msg_count % 1 == 0:
                velxyw = []
                vx = msg.linear.x
                vy = msg.linear.y
                wz = msg.angular.z
                print(t)
                velxyw.append(int(str(t))*0.000000001)
                velxyw.append(vx)
                velxyw.append(vy)
                velxyw.append(wz)
                writer2.writerow(velxyw)
    else:
        pass

def MO_parse(flag):
    if flag == True:
        bag_data = bag.read_messages("/robot2/motion")
        msg_count = 0
        f1 = open(out_dir + "motion.csv", 'w')
        writer1 = csv.writer(f1)

        for topic, msg, t in bag_data:
            msg_count = msg_count + 1
            if msg_count % 10 == 0:
                Mxyw = []
                vx = msg.Vx
                vy = msg.Vy
                wz = msg.Wz
                print(msg_count)
                Mxyw.append(int(str(t))*0.000000001)
                Mxyw.append(vx)
                Mxyw.append(vy)
                Mxyw.append(wz)
                writer1.writerow(Mxyw)
                
    else:
        pass

def NP_parse(flag):
    if flag == True:
        
        bag_data = bag.read_messages("/robot2NextState")
        msg_count = 0
        f1 = open(out_dir + "next_state.csv", 'w')
        writer1 = csv.writer(f1)


        for topic, msg, t in bag_data:
            msg_count = msg_count + 1
            if msg_count % 10 == 0:
                nsxyw = []
                x = msg.x
                y = msg.y
                theta = msg.theta
                print(msg_count)
                nsxyw.append(int(str(t))*0.000000001)
                nsxyw.append(x)
                nsxyw.append(y)
                nsxyw.append(theta)
                writer1.writerow(nsxyw)
                
    else:
        pass

def OO_parse(flag):
    if flag == True:
        
        bag_data1 = bag.read_messages("/robot1/odom")
        bag_data2 = bag.read_messages("/robot2/odom")
        bag_data3 = bag.read_messages("/wood/odom")
        
        f1 = open(out_dir + "robot1_odom.csv", 'w')
        writer1 = csv.writer(f1)
        f2 = open(out_dir + "robot2_odom.csv", 'w')
        writer2 = csv.writer(f2)
        f3 = open(out_dir + "wood_odom.csv", 'w')
        writer3 = csv.writer(f3)
        
        msg_count1 = 0
        for topic, msg, t in bag_data1:
            msg_count1 = msg_count1 + 1
            if msg_count1 % 10 == 0:
                xyw = []
                x = msg.twist.twist.linear.x
                y = msg.twist.twist.linear.y
                w = msg.twist.twist.angular.z
                print(msg_count1)
                xyw.append(int(str(t))*0.000000001)
                xyw.append(x)
                xyw.append(y)
                xyw.append(w)
                writer1.writerow(xyw)

        msg_count2 = 0
        for topic, msg, t in bag_data2:
            msg_count2 = msg_count2 + 1
            if msg_count2 % 10 == 0:
                xyw = []
                x = msg.twist.twist.linear.x
                y = msg.twist.twist.linear.y
                w = msg.twist.twist.angular.z
                print(msg_count2)
                xyw.append(int(str(t))*0.000000001)
                xyw.append(x)
                xyw.append(y)
                xyw.append(w)
                writer2.writerow(xyw)

        msg_count3 = 0
        for topic, msg, t in bag_data3:
            msg_count3 = msg_count3 + 1
            if msg_count3 % 10 == 0:
                xyw = []
                x = msg.twist.twist.linear.x
                y = msg.twist.twist.linear.y
                w = msg.twist.twist.angular.z
                print(msg_count3)
                xyw.append(int(str(t))*0.000000001)
                xyw.append(x)
                xyw.append(y)
                xyw.append(w)
                writer3.writerow(xyw)
                
    else:
        pass

def IMU_parse(flag):
    if flag == True:
        
        bag_data = bag.read_messages("/gazebo/link_states")
        msg_count = 0
        f1 = open(out_dir + "hand_pos.csv", 'w')
        writer1 = csv.writer(f1)
        f2 = open(out_dir + "slider_pos.csv", 'w')
        writer2 = csv.writer(f2)
        f3 = open(out_dir + "robot_pos.csv", 'w')
        writer3 = csv.writer(f3)

        for topic, msg, t in bag_data:
            msg_count = msg_count + 1
            if msg_count % 50 == 0:
                hpxy = []
                sdxy = []
                rxy = []
                hand_pos = msg.pose[list(msg.name).index("robot1::Link3")].position
                print(msg_count)
                print(hand_pos)
                hpxy.append(hand_pos.x)
                hpxy.append(hand_pos.y)
                writer1.writerow(hpxy)
                
                slider_pos = msg.pose[list(msg.name).index("robot2::Link4Slider")].position
                sdxy.append(slider_pos.x)
                sdxy.append(slider_pos.y)
                writer2.writerow(sdxy)

                robot_pos = msg.pose[list(msg.name).index("robot2::base_footprint")].position
                rxy.append(robot_pos.x)
                rxy.append(robot_pos.y)
                writer3.writerow(rxy)
    else:
        pass







if __name__ == "__main__":
    LS_parse(LS)
    TW_parse(TW)
    MO_parse(MO)
    NP_parse(NP)
    OO_parse(OO)
    IMU_parse(IMU)

