#include <ros/ros.h>
#include <Eigen/Core>
#include <sensor_msgs/PointCloud2.h>
#include <std_msgs/Float32.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/io/ply_io.h>
#include <pcl/common/transforms.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/conditional_removal.h>
#include "human_robot_transport/box_roi_compensate.hpp"

const float box1[4] = {-0.5, 0.5, -2.0, 2.0};
const float box2[4] = {-0.75, 0.75, -3, 3};
const float compensate_factor = 0.5;

using namespace std;


ros::Publisher callback_pub1;
ros::Publisher callback_pub2;
ros::Publisher callback_pub3;
ros::Publisher callback_pub4;


void BoxRoiCompensate::sub_callback(const sensor_msgs::PointCloud2ConstPtr& input, const float box[4], int pub_index)
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
        new pcl::FieldComparison<pcl::PointXYZ> ("x", pcl::ComparisonOps::GT, box[0])));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("x", pcl::ComparisonOps::LT, box[1])));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("y", pcl::ComparisonOps::GT, box[2])));
    range_cloud->addComparison(pcl::FieldComparison<pcl::PointXYZ>::ConstPtr (
        new pcl::FieldComparison<pcl::PointXYZ> ("y", pcl::ComparisonOps::LT, box[3])));
    pcl::ConditionalRemoval<pcl::PointXYZ> condrm;
    condrm.setCondition(range_cloud);
    condrm.setInputCloud(input_points);
    condrm.setKeepOrganized(true);
    condrm.filter(*output_points);

    pcl::toROSMsg(*output_points, output);
    
    std_msgs::Float32 y_compensate;
    Eigen::Vector4f centroid;
    pcl::compute3DCentroid(*output_points, centroid);
    y_compensate.data = centroid(1) * compensate_factor;

    switch (pub_index)
    {
    case 1:
        callback_pub1.publish(output);
        callback_pub3.publish(y_compensate);
        break;
    case 2:
        callback_pub2.publish(output);
        callback_pub4.publish(y_compensate);
        break;
    default:
        break;
    }
}



int main(int argc, char **argv)
{
    ros::init(argc, argv, "box_roi_compensate");
    ros::NodeHandle nh;
    callback_pub1 = nh.advertise<sensor_msgs::PointCloud2>("box1", 1);
    callback_pub2 = nh.advertise<sensor_msgs::PointCloud2>("box2", 1);
    callback_pub3 = nh.advertise<std_msgs::Float32>("compensate1", 1);
    callback_pub4 = nh.advertise<std_msgs::Float32>("compensate2", 1);

    ros::Subscriber pcl_sub1 = nh.subscribe<sensor_msgs::PointCloud2>("/PointCloud2", 1, boost::bind(BoxRoiCompensate::sub_callback, _1, box1, 1));
    ros::Subscriber pcl_sub2 = nh.subscribe<sensor_msgs::PointCloud2>("/PointCloud1", 1, boost::bind(BoxRoiCompensate::sub_callback, _1, box2, 2));

    ros::spin();
    return 0;
}