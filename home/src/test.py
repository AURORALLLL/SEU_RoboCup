#!/usr/bin/env python
# coding=UTF-8
import rospy
import cv2
import json
import os
import datetime
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from math import radians, pi
bridge = CvBridge()
count=0
num = 0
photo_flag = 0
image_topic = "/camera/rgb/image_raw"
savefolder_Path = r"/home/lynn/Robocup2022/Picture/shot"
def callback(msg):
    global count
    global photo_flag
    global num
    if photo_flag == 1:
    	print("OK")
    	rospy.loginfo("Goal succeeded!")
    	try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    	except CvBridgeError as e:
            print(e)
    	else:
	    if count != 0 and count != 4:
		num+=1
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(cv2_img,str(datetime.datetime.now()), (0, 20), font, 1, (0, 0, 255), 1)
        	cv2.putText(cv2_img,"11", (0, 60), font, 1, (0, 0, 255), 1)
                # Save your OpenCV2 image as a jpeg 	
                imgname="Image"+json.dumps(num)+".jpg"
    	        savePath=os.path.join(savefolder_Path,imgname)
    	        cv2.imwrite(savePath, cv2_img)
    	    count+=1
	    photo_flag = 0
    

class MoveBaseSquare():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        
        # How big is the square we want the robot to navigate?
        square_size = rospy.get_param("~square_size", 1.0) # meters
        
        # Create a list to hold the target quaternions (orientations)
        quaternions = list()
        
        # First define the corner orientations as Euler angles
        euler_angles = (pi/2, pi, 3*pi/2, 0)
        
        # Then convert the angles to quaternions
        for angle in euler_angles:
            q_angle = quaternion_from_euler(0, 0, angle, axes='sxyz')
            q = Quaternion(*q_angle)
            quaternions.append(q)
        
        # Create a list to hold the waypoint poses
        waypoints = list()
        
        # Append each of the four waypoints to the list.  Each waypoint
        # is a pose consisting of a position and orientation in the map frame.

        waypoints.append(Pose(Point(-3.64, -2.11, 0.0), quaternions[3]))#begin
        waypoints.append(Pose(Point(3.7, -1.5, 0.0), quaternions[3]))#1
        waypoints.append(Pose(Point(3.8, 1.15, 0.0), quaternions[3]))#2
        waypoints.append(Pose(Point(3.1, 1.1, 0.0), quaternions[1]))#3
	waypoints.append(Pose(Point(3.5, 0.4, 0.0), quaternions[1]))#
	#waypoints.append(Pose(Point(-1, 0.9, 0.0), quaternions[1]))#
        #waypoints.append(Pose(Point(1.32,-0.28, 0.0), quaternions[0]))#4
        waypoints.append(Pose(Point(-1.17,1.4, 0.0), quaternions[0]))#6
        waypoints.append(Pose(Point(-0.6,1.2, 0.0), quaternions[3]))#5


 # Initialize the visualization markers for RViz
        self.init_markers()
        
        # Set a visualization marker at each waypoint        
        for waypoint in waypoints:           
            p = Point()
            p = waypoint.position
            self.markers.points.append(p)
            
        # Publisher to manually control the robot (e.g. to stop it, queue_size=5)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=8)
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting navigation test")
        
        # Initialize a counter to track waypoints
        i = 0
        
        # Cycle through the four waypoints
        while i < 7 and not rospy.is_shutdown():
            # Update the marker display
            self.marker_pub.publish(self.markers)
            
            # Intialize the waypoint goal
            goal = MoveBaseGoal()
            rospy.loginfo("Starting navigation test")
            # Use the map frame to define goal poses
            goal.target_pose.header.frame_id = 'map'
            
            # Set the time stamp to "now"
            goal.target_pose.header.stamp = rospy.Time.now()
            
            # Set the goal pose to the i-th waypoint
            goal.target_pose.pose = waypoints[i]
            
            # Start the robot moving toward the goal
            self.move(goal)
            
            i += 1

    def move(self, goal):
	global photo_flag
        global count
        # Send the goal pose to the MoveBaseAction server
        self.move_base.send_goal(goal)
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(80)) 
            
        # If we don't get there in time, abort the goal
        if not finished_within_time:
            # We made it!
            self.move_base.cancel_goal()
	    count+=1
            rospy.loginfo("Timed out achieving goal")
	else:
	    state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
            	rospy.loginfo("Goal succeeded!")	
		photo_flag = 1	
		
                    
    def init_markers(self):
        # Set up our waypoint markers
        marker_scale = 0.2
        marker_lifetime = 0 # 0 is forever
        marker_ns = 'waypoints'
        marker_id = 0
        marker_color = {'r': 1.0, 'g': 0.7, 'b': 1.0, 'a': 1.0}
        
        # Define a marker publisher.
        self.marker_pub = rospy.Publisher('waypoint_markers', Marker, queue_size=5)
        
        # Initialize the marker points list.
        self.markers = Marker()
        self.markers.ns = marker_ns
        self.markers.id = marker_id
        self.markers.type = Marker.CUBE_LIST
        self.markers.action = Marker.ADD
        self.markers.lifetime = rospy.Duration(marker_lifetime)
        self.markers.scale.x = marker_scale
        self.markers.scale.y = marker_scale
        self.markers.color.r = marker_color['r']
        self.markers.color.g = marker_color['g']
        self.markers.color.b = marker_color['b']
        self.markers.color.a = marker_color['a']
        
        self.markers.header.frame_id = 'odom'
        self.markers.header.stamp = rospy.Time.now()
        self.markers.points = list()



    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        # Cancel any active goals
        self.move_base.cancel_goal()
        rospy.sleep(2)
        # Stop the robot
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    if not os.path.exists(savefolder_Path):
        os.makedirs(savefolder_Path)
    bridge = CvBridge()
    rospy.Subscriber(image_topic, Image,callback,queue_size=1)
    try:
        MoveBaseSquare()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
