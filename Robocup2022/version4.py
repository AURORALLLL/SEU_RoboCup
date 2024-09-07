#coding=UTF-8
import json
import base64
import cv2
import math
import time
import datetime
import os
import requests
from urllib import request
from urllib.parse import urlencode
            



#获取人脸access_token
def getToken():
    # 修改client_id和client_secret
    url_token='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xxxxxxxxxxxxxxxxxxxxx&client_secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    response= request.Request(url_token)
    response.add_header('Content-Type', 'application/json; charset=UTF-8')
    req= request.urlopen(response)
    content = req.read()
    if (content):
        token=json.loads(content)['access_token']
        return token


#图片base64转码
def getBase64(imgPath):
    with open(imgPath, "rb") as f: 
        base64_data = base64.b64encode(f.read()) 
        return base64_data

#人脸注册
def facelibUpload(imgBase64,token,imgName):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
    request_url = request_url + "?access_token=" + token
    r = request.Request(request_url)
    r.add_header('Content-Type', 'application/json')
    data = {"image": imgBase64,"image_type":"BASE64","group_id":"faceDetect","user_id": imgName}
    re = request.urlopen(r, urlencode(data).encode("utf-8"))
    content = re.read()
    if (content):
       print(content)
       print("Uploaded!!")


    
#人脸检测函数
def faceDetect(imgBase64,token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    request_url = request_url + "?access_token=" + token
    r = request.Request(request_url)
    r.add_header('Content-Type', 'application/json')
    data = {"image": imgBase64, "image_type": "BASE64","max_face_num":100,"face_field":"gender,quality"}
    re = request.urlopen(r, urlencode(data).encode("utf-8"))
    content = re.read()
    if (content):
        return content

#人脸对比函数
def facemultiSearch(imgBase64,token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/multi-search"
    request_url = request_url + "?access_token=" + token
    r = request.Request(request_url)
    r.add_header('Content-Type', 'application/json')
    data = {"image": imgBase64,"group_id_list": "faceDetect","image_type": "BASE64","max_face_num":10,"max_user_num":10}
    re = request.urlopen(r, urlencode(data).encode("utf-8"))
    content = re.read()
    if (content):
        return content

#性别显示
def genderWrite(imgBase64,token):
    return 0
    

#显示相关信息
def infoDisplay(face_list_detect,user_list,img,font):
    location=face_list_detect['location']
    gender=face_list_detect['gender']['type']
    #leftTopX=int(location['left'])
    #leftTopY=int(location['top'])
    #rightBottomX=int(leftTopX+int(location['width']))
    #rightBottomY = int(leftTopY + int(location['height']))
    #cv2.rectangle(img, (leftTopX, leftTopY), (rightBottomX, rightBottomY), (0, 255, 0), 2)   
    left=int(location['left'])
    top=int(location['top'])
    width=int(location['width'])
    height=int(location['height'])
    Theta = location['rotation'] / 60
    #为简化,实际为*pi/180
    A=(left,top)
    B=(int(left+math.cos(Theta)*width),int(top+math.sin(Theta)*width))
    C=(int(left-height*math.sin(Theta)),int(top+math.cos(Theta)*height))
    D=(int(left+math.cos(Theta)*width-math.sin(Theta)*height),int(top+math.sin(Theta)*width+math.cos(Theta)*height))
    cv2.line(img,A,B,(0, 255, 0), 2)
    cv2.line(img,B,D,(0, 255, 0), 2)
    cv2.line(img,A,C,(0, 255, 0), 2)
    cv2.line(img,C,D,(0, 255, 0), 2)
    cv2.putText(img,gender,A, font, 1, (0, 0, 255), 1)
    if (user_list):
        user_id=user_list[0]['user_id']
        cv2.putText(img,user_id, (left, top-15), font, 1, (0, 0, 255), 1)

 
if __name__ == '__main__':
    folder_Path = r"/home/lynn/Robocup2022/Picture"

    #上载人脸库
    facelib_Path = os.path.join(folder_Path,"Facelib")
    facelib_List = os.listdir(facelib_Path)
    for count in range(0,len(facelib_List)):
        img_Name = facelib_List[count]
        img_Path = os.path.join(facelib_Path,img_Name)
        facelibUpload(getBase64(img_Path),getToken(),os.path.splitext(img_Name)[0])
        time.sleep(3)
    #等待上载完成
    time.sleep(7)
    print("End of Uploading!!")

    #处理图片
    imgfolder_Path = os.path.join(folder_Path,"temp")
    img_List=os.listdir(imgfolder_Path)
    savefolder_Path=os.path.join(folder_Path,"face")
    if not os.path.exists(savefolder_Path):
        os.makedirs(savefolder_Path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for count in range(0,len(img_List)):
        img_Name = img_List[count]
        img_Path = os.path.join(imgfolder_Path,img_Name)
        result_Detect=json.loads(faceDetect(getBase64(img_Path),getToken()))['result']
        result_Search=json.loads(facemultiSearch(getBase64(img_Path),getToken()))['result']
        img = cv2.imread(img_Path, cv2.IMREAD_COLOR)
        #cv2.putText(img,str(datetime.datetime.now()), (0, 20), font, 0.5, (200, 255, 255), 1)
        if result_Detect and result_Search:
            for i in range(result_Detect['face_num']):
                facelist_Detect=result_Detect['face_list'][i]
                face_Probability=facelist_Detect['face_probability']
                if(face_Probability>0.98):
                    if(result_Search):
                        facelist_Search=result_Search['face_list'][i]
                        if facelist_Search:
                            userlist_Search = facelist_Search['user_list']
                            if userlist_Search:
                                if userlist_Search[0]['score'] > 80 :
                                    infoDisplay(facelist_Detect,userlist_Search,img,font)                        
        save_Path=os.path.join(savefolder_Path,img_Name)
        cv2.imwrite(save_Path,img)
    print("end")
