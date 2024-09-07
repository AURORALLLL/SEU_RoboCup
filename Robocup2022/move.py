# -*- coding:utf-8 -*-
import os
import shutil

if __name__ == '__main__':
    imgfolder_Path = r"/home/lynn/Robocup2022/Picture/Img"
    img_List=os.listdir(imgfolder_Path)
    for count in range(0,len(img_List)):
        img_Name = img_List[count]
        #img_Path = os.path.join(imgfolder_Path,img_Name)
        if img_Name == "Image1.jpg":
            img_Path = os.path.join(imgfolder_Path,img_Name)
            save_Path = r"/home/lynn/catkin_ws/src/home/models/mark_label1/materials/textures"
            dst = os.path.join(save_Path,img_Name)
        if img_Name == "Image2.jpg":
            img_Path = os.path.join(imgfolder_Path,img_Name)
            save_Path = r"/home/lynn/catkin_ws/src/home/models/mark_label2/materials/textures"
            dst = os.path.join(save_Path,img_Name)
        if img_Name == "Image3.jpg":
            img_Path = os.path.join(imgfolder_Path,img_Name)
            save_Path = r"/home/lynn/catkin_ws/src/home/models/mark_label6/materials/textures"
            img_Name = "Image6.jpg"
            dst = os.path.join(save_Path,img_Name)
        if img_Name == "Image4.jpg":
            img_Path = os.path.join(imgfolder_Path,img_Name)
            save_Path = r"/home/lynn/catkin_ws/src/home/models/mark_label4/materials/textures"
            dst = os.path.join(save_Path,img_Name)
        if img_Name == "Image5.jpg":
            img_Path = os.path.join(imgfolder_Path,img_Name)
            save_Path = r"/home/lynn/catkin_ws/src/home/models/mark_label5/materials/textures"
            dst = os.path.join(save_Path,img_Name)
        shutil.copyfile(img_Path,dst)