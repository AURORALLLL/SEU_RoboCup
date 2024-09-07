import numpy as np
import cv2
import os

def adjust_brightness(img, brightness_factor):
    # clip(0, 255)会把处理后的像素值的大小，现在在[0, 255]范围内，如果有值大于255则取255,如果有值小于0则取值0
    table = np.array([i * brightness_factor for i in range (0,256)]).clip(0,255).astype('uint8')
    # 单通道img
    if img.shape[2] == 1:
        return cv2.LUT(img, table)[:,:,np.newaxis]
    # 多通道img
    else:
        result = cv2.LUT(img, table)
        return result

def get_lightness(src):
    hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    lightness = hsv_image[:,:,2].mean()
    return  lightness



if __name__ == '__main__':
    imgpath = r"/home/lynn/Robocup2022/Picture/shot"
    savepath = r"/home/lynn/Robocup2022/Picture/temp"
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    img_List=os.listdir(imgpath)
    for count in range(0,len(img_List)):
        img_Name = img_List[count]
        img_Path = os.path.join(imgpath,img_Name)
        img = cv2.imread(img_Path)
        lightness = get_lightness(img)
        # 自适应调整亮度
        if lightness > 0:
            re=adjust_brightness(img, brightness_factor=175/lightness)
        else:
            re=adjust_brightness(img, brightness_factor=4)
        save_Path=os.path.join(savepath,img_Name)
        cv2.imwrite(save_Path, re)
