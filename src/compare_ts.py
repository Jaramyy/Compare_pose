#!/usr/bin/env python

import rosbag
import message_filters
import rospy
from nav_msgs.msg import Odometry
import tf
import threading

n=0
error = []

def timeout():
    print("Time out")
    print(n)

def callback(odom_optic_sub, odom_rs_sub):
    global timer
    global n
    n=n+1
    #print("msg = ",odom_rs_sub.pose.pose.position)
    error_x = odom_rs_sub.pose.pose.position.x - odom_optic_sub.pose.pose.position.x
    error_y = odom_rs_sub.pose.pose.position.y - odom_optic_sub.pose.pose.position.y
    error_z = odom_rs_sub.pose.pose.position.z - odom_optic_sub.pose.pose.position.z
    error.append([error_x,error_y,error_z])
    print("error = ",n)
    timer.cancel()
    timer = threading.Timer(2,timeout)
    timer.start()
    

if __name__ == "__main__":
    rospy.init_node('compare_node') 
    odom_optic_sub = message_filters.Subscriber('/camera/odom/sample',Odometry)
    odom_rs_sub = message_filters.Subscriber('/camera/odom/sample',Odometry)
    ts = message_filters.TimeSynchronizer([odom_optic_sub,odom_rs_sub],10)  
    #ts = message_filters.ApproximateTimeSynchronizer([odom_optic_sub,odom_rs_sub], 10, 1, allow_headerless=False)
    ts.registerCallback(callback)    
    timer = threading.Timer(2,timeout)
    timer.start()
    rospy.spin()