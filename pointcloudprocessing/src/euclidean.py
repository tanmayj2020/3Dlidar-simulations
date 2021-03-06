#! /usr/bin/env python3
import rospy
from sensor_msgs.msg import PointCloud2
 
import pcl
import pcl_helper
def do_euclidian_clustering(cloud):
 # Euclidean Clustering
    white_cloud = pcl_helper.XYZRGB_to_XYZ(cloud) # <type 'pcl._pcl.PointCloud'>
    tree = white_cloud.make_kdtree() # <type 'pcl._pcl.KdTree'>
    ec = white_cloud.make_EuclideanClusterExtraction()
    ec.set_ClusterTolerance(0.02) # for hammer
    ec.set_MinClusterSize(10)
    ec.set_MaxClusterSize(250)
    ec.set_SearchMethod(tree)
    cluster_indices = ec.Extract() # indices for each cluster (a list of lists)
    # Assign a color to each cluster
    cluster_color = pcl_helper.random_color_gen()
    #cluster_color = pcl_helper.get_color_list(len(cluster_indices))
    color_cluster_point_list = []
    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            color_cluster_point_list.append([white_cloud[indice][0], white_cloud[indice][1], white_cloud[indice][2], pcl_helper.rgb_to_float(cluster_color)])
    # Create new cloud containing all clusters, each with unique color
    cluster_cloud = pcl.PointCloud_PointXYZRGB()
    cluster_cloud.from_list(color_cluster_point_list)
    # publish to cloud
    ros_cluster_cloud = pcl_helper.pcl_to_ros(cluster_cloud)    
    return cluster_cloud
def callback(input_ros_msg):
    cloud = pcl_helper.ros_to_pcl(input_ros_msg)
    cloud = do_euclidian_clustering(cloud)
    cloud_new = pcl_helper.pcl_to_ros(cloud)
    pub.publish(cloud_new)
if __name__ == '__main__':
 rospy.init_node("euclidean" , anonymous= True)
 rospy.Subscriber("/velodyne" , PointCloud2 , callback)
 pub = rospy.Publisher("/velodyne_new" , PointCloud2 , queue_size=1)
 rospy.spin()