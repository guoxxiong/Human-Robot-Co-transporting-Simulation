#include<ros/ros.h>
#include<sensor_msgs/PointCloud2.h>
#include<pcl_conversions/pcl_conversions.h>
#include<pcl/point_cloud.h>
#include<pcl/point_types.h>
#include<pcl/filters/conditional_removal.h>
#include<visualization_msgs/MarkerArray.h>
#include"human_robot_transport/roi.hpp"

using namespace std;

ros::Publisher points_pub;
ros::Publisher callback_pub1;
ros::Publisher callback_pub2;
ros::Publisher callback_pub3;
ros::Publisher callback_pub4;
ros::Publisher callback_pub5;
ros::Publisher callback_pub6;
ros::Publisher callback_pub7;
ros::Publisher callback_pub8;

const double G_THS = 0.02;
const double THS1 = 0.2;
const double THS2 = 0.4;
const double THS3 = 0.6;
const double THS4 = 0.8;
const double THS5 = 1.0;
const double THS6 = 1.2;
const double THS7 = 1.4;
const double THS8 = 1.6;

void ground_filter(const sensor_msgs::PointCloud2ConstPtr& input)
{
    /*data struct defining*/
    sensor_msgs::PointCloud2 output;
    pcl::PointCloud<pcl::PointXYZ>::Ptr input_points(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr output_points(new pcl::PointCloud<pcl::PointXYZ>);

    /*format converting*/
    pcl::fromROSMsg(*input, *input_points);

    /*filtering*/
    pcl::ConditionAnd<pcl::PointXYZ>::Ptr range_cloud(
        new pcl::ConditionAnd<pcl::PointXYZ>());
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("z", pcl::ComparisonOps::GT, G_THS)));
    pcl::ConditionalRemoval<pcl::PointXYZ> condrm;
    condrm.setCondition(range_cloud);
    condrm.setInputCloud(input_points);
    condrm.setKeepOrganized(true);
    condrm.filter(*output_points);

    pcl::toROSMsg(*output_points, output);
    points_pub.publish(output);
}

void cut_off(const sensor_msgs::PointCloud2ConstPtr& input, const double minths, const double maxths, const double roi[], int pub_index)
{
    /*data struct defining*/
    sensor_msgs::PointCloud2 output;
    pcl::PointCloud<pcl::PointXYZ>::Ptr input_points(new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr output_points(new pcl::PointCloud<pcl::PointXYZ>);

    /*format converting*/
    pcl::fromROSMsg(*input, *input_points);

    /*filtering*/
    pcl::ConditionAnd<pcl::PointXYZ>::Ptr range_cloud(
        new pcl::ConditionAnd<pcl::PointXYZ>());
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("z", pcl::ComparisonOps::GT, minths)));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("z", pcl::ComparisonOps::LT, maxths)));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("x", pcl::ComparisonOps::GT, roi[0])));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("x", pcl::ComparisonOps::LT, roi[1])));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("y", pcl::ComparisonOps::GT, roi[2])));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("y", pcl::ComparisonOps::LT, roi[3])));
    pcl::ConditionalRemoval<pcl::PointXYZ> condrm;
    condrm.setCondition(range_cloud);
    condrm.setInputCloud(input_points);
    condrm.setKeepOrganized(true);
    condrm.filter(*output_points);

    pcl::toROSMsg(*output_points, output);

    switch (pub_index)
    {
    case 1:
        callback_pub1.publish(output);
        break;
    case 2:
        callback_pub2.publish(output);
        break;
    case 3:
        callback_pub3.publish(output);
        break;
    case 4:
        callback_pub4.publish(output);
        break;
    case 5:
        callback_pub5.publish(output);
        break;
    case 6:
        callback_pub6.publish(output);
        break;
    case 7:
        callback_pub7.publish(output);
        break;
    case 8:
        callback_pub8.publish(output);
        break;
    default:
        break;
    }
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "ground_filter");
    ros::NodeHandle nh;
    points_pub = nh.advertise<sensor_msgs::PointCloud2>("no_ground_points", 1);
    callback_pub1 = nh.advertise<sensor_msgs::PointCloud2>("field1", 1);
    callback_pub2 = nh.advertise<sensor_msgs::PointCloud2>("field2", 1);
    callback_pub3 = nh.advertise<sensor_msgs::PointCloud2>("field3", 1);
    callback_pub4 = nh.advertise<sensor_msgs::PointCloud2>("field4", 1);
    callback_pub5 = nh.advertise<sensor_msgs::PointCloud2>("field5", 1);
    callback_pub6 = nh.advertise<sensor_msgs::PointCloud2>("field6", 1);
    callback_pub7 = nh.advertise<sensor_msgs::PointCloud2>("field7", 1);
    callback_pub8 = nh.advertise<sensor_msgs::PointCloud2>("field8", 1);
    ros::Subscriber pcl_sub = nh.subscribe<sensor_msgs::PointCloud2>("/velodyne_points", 1, ground_filter);
    ros::Subscriber pcl_sub1 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, G_THS, THS1, ROI1, 1));
    ros::Subscriber pcl_sub2 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, THS1, THS2, ROI1, 2));
    ros::Subscriber pcl_sub3 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, THS2, THS3, ROI1, 3));
    ros::Subscriber pcl_sub4 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, THS3, THS4, ROI1, 4));
    ros::Subscriber pcl_sub5 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, THS4, THS5, ROI1, 5));
    ros::Subscriber pcl_sub6 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, THS5, THS6, ROI1, 6));
    ros::Subscriber pcl_sub7 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, THS6, THS7, ROI1, 7));
    ros::Subscriber pcl_sub8 = nh.subscribe<sensor_msgs::PointCloud2>("/no_ground_points", 1, boost::bind(cut_off, _1, THS7, THS8, ROI1, 8));
    std::cout << "The Point Cloud has been segmented!" << std::endl;
    ros::spin();
    return 0;
}