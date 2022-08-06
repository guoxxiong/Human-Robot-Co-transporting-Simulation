#include"human_robot_transport/roi.hpp"
#include<ros/ros.h>
#include<visualization_msgs/Marker.h>
#include<visualization_msgs/MarkerArray.h>

visualization_msgs::MarkerArray generate_roi(const double position[3][4], int level)
{
    visualization_msgs::MarkerArray costCubes;
    for (int i = 0; i < 3; i++)
    {
        visualization_msgs::Marker costCube;
        costCube.action = visualization_msgs::Marker::ADD;
        costCube.header.frame_id = "robot2/velodyne";
        costCube.header.stamp = ros::Time::now();
        costCube.id = i;
        costCube.type =  visualization_msgs::Marker::CUBE;
        costCube.scale.x = position[i][1] - position[i][0];
        costCube.scale.y = position[i][3] - position[i][2];
        costCube.scale.z = 0.2;
        costCube.color.a = (i + 1) * 0.05;
        switch (level)
        {
        case 1:
            costCube.color.r = 255;
            costCube.color.g = 255;
            costCube.color.b = 255;
            break;
        case 2:
            costCube.color.r = 0;
            costCube.color.g = 0;
            costCube.color.b = 255;
            break;
        case 3:
            costCube.color.r = 0;
            costCube.color.g = 255;
            costCube.color.b = 0;
            break;
        case 4:
            costCube.color.r = 0;
            costCube.color.g = 255;
            costCube.color.b = 255;
            break;
        case 5:
            costCube.color.r = 255;
            costCube.color.g = 0;
            costCube.color.b = 0;
            break;
        case 6:
            costCube.color.r = 255;
            costCube.color.g = 0;
            costCube.color.b = 255;
            break;
        case 7:
            costCube.color.r = 255;
            costCube.color.g = 255;
            costCube.color.b = 0;
            break;
        case 8:
            costCube.color.r = 255;
            costCube.color.g = 255;
            costCube.color.b = 255;
            break;
        default:
            break;
        }
        costCube.pose.position.x = 0.5 * (position[i][0] + position[i][1]);
        costCube.pose.position.y = 0.5 * (position[i][2] + position[i][3]);
        costCube.pose.position.z = level * 0.2 - 0.1;
        costCubes.markers.push_back(costCube);
    }
    return costCubes;
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "roi_marker_pub");
    ros::NodeHandle nh;
    ros::Publisher markerArrayPub1 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level1", 1);
    ros::Publisher markerArrayPub2 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level2", 1);
    ros::Publisher markerArrayPub3 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level3", 1);
    ros::Publisher markerArrayPub4 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level4", 1);
    ros::Publisher markerArrayPub5 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level5", 1);
    ros::Publisher markerArrayPub6 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level6", 1);
    ros::Publisher markerArrayPub7 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level7", 1);
    ros::Publisher markerArrayPub8 = nh.advertise<visualization_msgs::MarkerArray>("roi_of_level8", 1);
    visualization_msgs::MarkerArray roi_of_level1, roi_of_level2, roi_of_level3, roi_of_level4, 
    roi_of_level5, roi_of_level6, roi_of_level7, roi_of_level8; 
    roi_of_level1 = generate_roi(ROI, 1);
    roi_of_level2 = generate_roi(ROI, 2);
    roi_of_level3 = generate_roi(ROI, 3);
    roi_of_level4 = generate_roi(ROI, 4);
    roi_of_level5 = generate_roi(ROI, 5);
    roi_of_level6 = generate_roi(ROI, 6);
    roi_of_level7 = generate_roi(ROI, 7);
    roi_of_level8 = generate_roi(ROI, 8);
    ros::Rate rate(10.0);
    while (ros::ok())
    {
        markerArrayPub1.publish(roi_of_level1);
        markerArrayPub2.publish(roi_of_level2);
        markerArrayPub3.publish(roi_of_level3);
        markerArrayPub4.publish(roi_of_level4);
        markerArrayPub5.publish(roi_of_level5);
        markerArrayPub6.publish(roi_of_level6);
        markerArrayPub7.publish(roi_of_level7);
        markerArrayPub8.publish(roi_of_level8);
        rate.sleep();
    }
    return 0;
}