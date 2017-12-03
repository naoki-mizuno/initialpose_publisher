#!/usr/bin/env python2

import rospy
import tf2_ros

from geometry_msgs.msg import PoseWithCovarianceStamped

rospy.init_node('initialpose_publisher')

buf = tf2_ros.Buffer()
tf_l = tf2_ros.TransformListener(buf)

map_frame_id = rospy.get_param('~map_frame_id', 'map')
base_frame_id = rospy.get_param('~base_frame_id', 'base_link')
topic_name = rospy.get_param('~topic_name', 'initialpose')
rate = rospy.Rate(rospy.get_param('~hz', 10))

initialpose_pub = rospy.Publisher(topic_name, PoseWithCovarianceStamped, queue_size=1)


def publish_pose(map_frame_id, base_frame_id, topic_name):
    global buf

    try:
        transform = buf.lookup_transform(map_frame_id,
                                         base_frame_id,
                                         rospy.Time(0),
                                         rospy.Duration(0.05))
    except tf2_ros.TransformException:
        return

    pose = PoseWithCovarianceStamped()
    pose.header = transform.header
    p = pose.pose.pose
    p.position.x = transform.transform.translation.x
    p.position.y = transform.transform.translation.y
    p.position.z = transform.transform.translation.z
    p.orientation.x = transform.transform.rotation.x
    p.orientation.y = transform.transform.rotation.y
    p.orientation.z = transform.transform.rotation.z
    p.orientation.w = transform.transform.rotation.w
    initialpose_pub.publish(pose)

if __name__ != '__main__':
    sys.stderr('This program needs to be run as a script')
    exit(1)

while not rospy.is_shutdown():
    try:
        publish_pose(map_frame_id, base_frame_id, topic_name)
        rate.sleep()
    except rospy.exceptions.ROSInterruptException:
        print('Bye!')
        exit(0)

