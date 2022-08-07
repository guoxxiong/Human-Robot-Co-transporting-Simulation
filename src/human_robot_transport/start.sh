xterm -e "roscore" &
sleep 5

xterm -e "roslaunch human_robot_transport CoTransportMech.launch" &
sleep 8

xterm -e "roslaunch human_robot_transport functions2.launch" &
sleep 5

xterm -e "ROS_NAMESPACE=robot1 rosrun teleop_twist_keyboard teleop_twist_keyboard.py"
