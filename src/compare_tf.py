#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import tf
import tf2_ros
from geometry_msgs.msg import PoseStamped
import matplotlib.pyplot as plt
import threading
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


if __name__ == '__main__':
    rospy.init_node('compare_tf')
    #ax = plt.axes(projection='3d')
    
    fig = plt.figure(figsize=(16,9))
    ax = fig.add_subplot(1,1,1, projection='3d')
    tfBuffer = tf2_ros.Buffer(cache_time=rospy.Duration(10.0))
    listener = tf2_ros.TransformListener(tfBuffer,queue_size=None, buff_size=65535, tcp_nodelay=False)
    #listener = tf.TransformListener()
    #listener2 = tf.TransformListener()
    #plt.ion()
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #sum_error = np.zeros(1)
    sum_error = 0
    num = 0
    rate = rospy.Rate(500)
    while not rospy.is_shutdown():
        try:
            #if tfBuffer.can_transform('world','Drone_link',rospy.Time(0)):
            #    print("can")
            #else:
            
            # (tran,rot) = listener.lookupTransform('world','Drone_link',rospy.Time(0))
            tran2 = tfBuffer.lookup_transform('world','drone_link',rospy.Time(0),rospy.Duration(3.0))
            # (tran2,rot2) = listener.lookupTransform('world','Drone',rospy.Time(0)) 
            tran = tfBuffer.lookup_transform('world','Drone',rospy.Time(0),rospy.Duration(3.0)) 
            #(tran2,rot2) = listener2.lookupTransform('world','Drone',rospy.Time(0))
            #plt.plot(tran[0],tran[1],color="red") 
            #print("tran = ",tran)
            #print("tran2 = ",tran2)
            print("calculating...")
            print("z = ",tran.transform.translation.z)
            #if tran.transform.translation.z > 1.2:
            ax.scatter(tran.transform.translation.x,tran.transform.translation.y,tran.transform.translation.z, marker="x", c="red")
            ax.scatter(tran2.transform.translation.x,tran2.transform.translation.y,tran2.transform.translation.z ,marker="o", c="green")
            #else:
            #    ax.scatter(tran.transform.translation.x,tran.transform.translation.y,tran.transform.translation.z, marker="x", c="yellow")
            #    ax.scatter(tran2.transform.translation.x,tran2.transform.translation.y,tran2.transform.translation.z ,marker="o", c="blue")

            error_x = tran.transform.translation.x - tran2.transform.translation.x
            error_y = tran.transform.translation.y - tran2.transform.translation.y
            error_z = tran.transform.translation.z - tran2.transform.translation.z
            error_dis = math.sqrt(math.pow(error_x,2)+math.pow(error_y,2)+math.pow(error_z,2))
            error_dis_pow = math.pow(error_dis,2)
            
            sum_error = sum_error + error_dis_pow
            num = num + 1
            #sum_error = np.append(sum_error,error_dis)
            #print(tfBuffer)
            #print(sum_error)
            #print("size= ",np.shape(sum_error))
            print(num)
            tfBuffer.clear()            
        
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            print("no tf incoming")
            if num == 0:
                print("err num = 0")
                continue
            #rate.sleep()   
            #pass
        rate.sleep()
    print("result:") 
    percent_error = math.sqrt(sum_error/num)
    print("sum_error = ",sum_error)
    print("num = ",num)
    print("RMSE = ",percent_error)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')           
    
    #ax.dist = 10
    plt.savefig("trajectory1.png",dpi=500)
    ax.view_init(elev=0, azim=90)
    #ax.dist = 10
    plt.savefig("trajectory2.png" ,dpi=500)
    ax.view_init(elev=90, azim=0)
    #ax.dist = 10
    plt.savefig("trajectory3.png" ,dpi=500)
    plt.show()
    
    
    
  