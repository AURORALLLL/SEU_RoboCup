# -*- coding:utf-8 -*-
import roslaunch
import rospy
import time
import os
folder_Path = r"/home/lynn/Robocup2022/Picture/shot"
time_start=time.time()
# 开启gazebo,机器人
uuid1 = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid1)
tracking_launch1 = roslaunch.parent.ROSLaunchParent(
    uuid1, ["/home/lynn/catkin_ws/src/home/launch/step1.launch"])
tracking_launch1.start()
time.sleep(13)

# 启动导航
uuid2 = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid2)
tracking_launch2 = roslaunch.parent.ROSLaunchParent(
    uuid2, ["/home/lynn/catkin_ws/src/home/launch/step2.launch"])
tracking_launch2.start()

# 判断是否拍摄到五张图像，拍摄到/超时及终止程序
while (1):
    time_end=time.time()
    length = len(os.listdir(folder_Path))
    if length == 5:
        tracking_launch2.shutdown()
        break
    if time_end-time_start >480:
        tracking_launch2.shutdown()
        break
