#!/usr/bin/env python2

import rospy
import tf2_ros

from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped

import sys


if __name__ != '__main__':
    sys.stderr('This program needs to be run as a script')
    exit(1)

rospy.init_node('initialpose_publisher')

buf = tf2_ros.Buffer()
tf_l = tf2_ros.TransformListener(buf)

map_frame_id = rospy.get_param('~map_frame_id', 'map')
base_frame_id = rospy.get_param('~base_frame_id', 'base_link')
topic_name = rospy.get_param('~topic_name', 'initialpose')


def goal_sub(msg):
    publish_pose(map_frame_id, base_frame_id)


initialpose_pub = rospy.Publisher(topic_name, PoseWithCovarianceStamped, queue_size=1)
goal_sub = rospy.Subscriber('move_base_simple/goal', PoseStamped, goal_sub, queue_size=1)


def publish_pose(map_frame_id, base_frame_id):
    global buf

    while True:
        try:
            transform = buf.lookup_transform(map_frame_id,
                                             base_frame_id,
                                             rospy.Time(0),
                                             rospy.Duration(3))
            break
        except tf2_ros.TransformException as e:
            rospy.logerr(e)
            continue

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


rospy.spin()
