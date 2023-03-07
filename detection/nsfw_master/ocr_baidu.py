# encoding:utf-8

import requests
import base64
import json
import cv2
import os
import re
import string
string.punctuation




'''
网络图片文字识别
'''


#输入图片地址
#返回文本列表
def ocr(image_path):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
    # 二进制方式打开图片文件
    f = open(image_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = '24.edb7c86bb6750685f3fbb8187306da73.2592000.1680236619.282335-30849076'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
    #将字典中所要的值转换成列表
    dict = response.json()
    list = dict.get('words_result')
    newlist = []
    for item in list:
        newlist.append(item['words'])
    #print(newlist)
    return newlist



def changeImage(path, pra):
    img = cv2.imread(path, 1)
    #pra为缩放的倍率
    width,height  = img.shape[:2]
    #此处要做integer强转,因为.resize接收的参数为形成新图像的长宽像素点个数
    size = (int(height*pra), int(width*pra))
    img_new = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    os.path.join('nsfw_master\data', '11.jpg')  # 保存的图片与原始图片同名

    return 'nsfw_master/data'+ '/11'



# 违规文字匹配
# 输入违规文字库地址 ，检测文字
# 输出违规提示文本列表
def text_maching(path, text):
    fname = path
    resulList = []
    finallist = []
    punctuation_string = string.punctuation

    with open(fname, mode='r',  encoding='utf-8', errors='ignore') as f:  # 打开文件
        lines = f.readlines()  # 读取所有行

        l = len(lines)

        for i in range(0, l):
            pattern = lines[i][:-1]  # 读取第l行
            pattern = re.findall('[\w]+', pattern)
            pattern = "".join(pattern)
            if pattern.isspace() or pattern == '':
                continue
            # pattern = '(\''+pattern+'\')'
            #print(pattern,'-'*7)


            if pattern in text:
                resulList.append(lines[i])
            i += 1

            for data in resulList:
                sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",data)
                finallist.append(sub_str)
    finallist = list(set(finallist))
    return finallist

'''
文本审核接口
'''
#输入待审核文本，输出结论文本
#限制字符长度6666
def text_moderation(text_raw):
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"

    params = {"text": text_raw}
    access_token = '24.ef1e201a068c1fc606fe2969ae840a12.2592000.1680685179.282335-31010735'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    message = '合格'
    if response:
        print(response.json())
    else:
        print("文本审核失败！")

    dict = response.json()
    conclusion =  dict.get('conclusion')

    if conclusion == '合规':
        print('1111111111111111111111')
        message = '合格'

    else:
        print('2222222222222222222222')
        list = dict.get('data')
        #print(list)
        msg = ''
        keywords = []
        for data in list:
            keywords = data['hits']
            msg = data['msg']
            #print(keywords)
        for data2 in keywords:
            msg = msg +",违规词："+str(data2['words'])

        message ='图片不合格 : '+msg

    print(message)
    return message



if  __name__ == '__main__':
    #image = 'C:/Users/汤思源/Desktop/IMG_5177(20230220-232409).JPG'
    #ocr(image)
    str = changeImage('./culturelle.jpg', 0.2)
    print(str)
    # list = ocr(str)
    # print(list)

