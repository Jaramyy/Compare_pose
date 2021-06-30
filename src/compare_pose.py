#!/usr/bin/env python
from nav_msgs import msg
import rospy
import rosbag
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped


bag1 = rosbag.Bag('2021-05-24-18-37-17.bag')
bag2 = rosbag.Bag('2021-05-24-18-37-17.bag')

bag1_d=[] 
bag2_d=[]

def read_bag(topic):
    for topic, msg, t in bag1.read_messages(topics=[topic]):
        bag1_d.append([t.nsecs,msg.pose.pose.position.x,msg.pose.pose.position.y,msg.pose.pose.position.z])
    bag1.close()
    return bag1_d
    
if __name__ == '__main__':
    n=0
    for topic, msg, t in bag1.read_messages(topics=['/camera/odom/sample']):
        #print(msg)
        bag1_d.append([t.nsecs,msg.pose.pose.position.x])
        bag2_d.append([t.nsecs,msg.pose.pose.position.y])
        #a = t.nsecs
        #b = t.nsecs
        #if a == b:
        #    print("bag1",n)
        #    n = n+1
            #print(msg)
            #rospy.sleep(0.002)
        #print(t.nsecs)
    bag1.close()
    #rospy.sleep(2)
    for (a1,b1),(a2,b2) in zip(bag1_d,bag2_d):
        print("a1 =",a1,"a2 = ",a2) 
        if a1 == a2:
            n=n+1
            print(n)
        #rospy.sleep(0.1)
    #bag2.close()
        
#[(time,x,y,z),(time,x,y,z),(time,x,y,z),(time,x,y,z)]