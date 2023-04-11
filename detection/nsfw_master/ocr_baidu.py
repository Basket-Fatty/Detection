# encoding:utf-8

import requests
import base64
import json
import os
import re
import string
string.punctuation
from DFA import *
from PIL import Image
import math
import cv2

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
    access_token = '24.900e8ceaafc5011d91a1df481ca4ae15.2592000.1683374449.282335-32072986'
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



# def changeImage(path, pra):
#     # img = cv2.imread(path, 1)
#     #pra为缩放的倍率
#     width,height  = img.shape[:2]
#     #此处要做integer强转,因为.resize接收的参数为形成新图像的长宽像素点个数
#     size = (int(height*pra), int(width*pra))
#     # img_new = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
#     os.path.join('nsfw_master\data', '11.jpg')  # 保存的图片与原始图片同名
#
#     return 'nsfw_master/data'+ '/11'



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
#此为下策，现在接口应该已经过期了
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

# 翻译函数，word 需要翻译的内容
def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        return response.text
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None

def get_reuslt(repsonse):
    # 通过 json.loads 把返回的结果加载成 json 格式
    result = json.loads(repsonse)
    # print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
    # print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
    str =result['translateResult'][0][0]['tgt']

    return str

#写入txt函数,输入的是列表
def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'w',encoding='utf-8')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")

#有道翻译接口，输入中文文本，返回英文文本
def translate_youdao(word):
    list_trans = translate(word)
    str = get_reuslt(list_trans)
    return  str

#切割图片
def produceImage(file_in, width, height, file_out):
    image = Image.open(file_in)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)


"""
This is a large image ocr function.

Parameters:
 param1 - Image address

Returns:
 Return a text list
"""
def final_ocr(image_path):
    im = Image.open(image_path)
    img_size = im.size
    m = img_size[0]  # 读取图片的宽度
    n = img_size[1]  # 读取图片的高度
    w = 10  # 设置你要裁剪的小图的宽度
    h = 10  # 设置你要裁剪的小图的高度

    image_num = math.ceil(n/4096)
    for i in range(image_num):  # 裁剪为100张随机的小图
        if (i+1)*4096 < n:
            region = im.crop((0, i*4096, m, (i+1)*4096) ) # 裁剪区域
        else:
            region = im.crop((0, i * 4096, m, n))  # 裁剪区域

        region.save("" + str(i) + ".jpg")  # str(i)是裁剪后的编号，此处是0到99

    #根据切的份数，进行ocr
    resultlist = []
    for i in range(image_num):
        resultlist = resultlist +ocr("" + str(i) + ".jpg")

    return resultlist


if  __name__ == '__main__':
    imagepath ="C:/Users/10570/Desktop/毕设/FinancialMediaDetection-v2/FinancialMediaDetection/detection/data/small_picture/3D蒸汽热敷眼罩(1).jpg"
    list = ocr(imagepath)
    text_save("text.txt",list)
    run("text.txt")



