#ifndef BOX_ROI_COMPENSATE_H
#define BOX_ROI_COMPENSATE_H

#include<sensor_msgs/PointCloud2.h>
#include<std_msgs/Float32.h>

class BoxRoiCompensate
{
    public:
    BoxRoiCompensate();
    static void sub_callback(const sensor_msgs::PointCloud2ConstPtr& input, const float box[4], int pub_index);
};


#endif