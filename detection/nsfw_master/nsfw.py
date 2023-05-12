#
# # encoding:utf-8
#
# import requests
# import base64
#
# '''
# 图像审核接口
# '''
#
# request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
# # 二进制方式打开图片文件
# f = open('images.jpg', 'rb')
# img = base64.b64encode(f.read())
#
# params = {"image":img}
# access_token = '24.6bf8afc89f699191c33f13fee714a6bb.2592000.1686415280.282335-33441629'
# request_url = request_url + "?access_token=" + access_token
# headers = {'content-type': 'application/x-www-form-urlencoded'}
# response = requests.post(request_url, data=params, headers=headers)
# if response:
#     print (response.json())
import requests
import base64
from PIL import Image
import math
from ocr_baidu import  translate

def check_image_safety(image_path):
    # 读取图片文件并进行 base64 编码
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # 设置请求参数和请求头
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
    access_token = '24.6bf8afc89f699191c33f13fee714a6bb.2592000.1686415280.282335-33441629'
    params = {"image": image_base64}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    request_url = url + "?access_token=" + access_token

    # 发送请求并处理响应
    response = requests.post(request_url, data=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        conclusion = result['conclusion']
        if conclusion == "合规":
            msg = "无"
        else:
            msg = result['data'][0]['msg']
    else:
        conclusion = "请求错误"
        msg ="请求错误"

    return (conclusion, msg)


def final_ocr2(image_path):
    im = Image.open(image_path)
    img_size = im.size
    m = img_size[0]  # 读取图片的宽度
    n = img_size[1]  # 读取图片的高度

    image_num = math.ceil(n/4096)
    for i in range(image_num):  # 裁剪为100张随机的小图
        if (i+1)*4096 < n:
            region = im.crop((0, i*4096, m, (i+1)*4096) ) # 裁剪区域
        else:
            region = im.crop((0, i * 4096, m, n))  # 裁剪区域
        if region.mode == "RGBA":
            region = region.convert('RGB')

        region.save("" + str(i) + ".jpg")  # str(i)是裁剪后的编号，此处是0到99


    #根据切的份数，进行ocr
    return_str = ""
    checkResult = ''
    for i in range(image_num):
        checkResult = check_image_safety("" + str(i) + ".jpg")
        if checkResult[0] == "不合规" or checkResult[0] == "请求错误":
            return_str = 'The images contain sexual content'
            break
    if checkResult[0] == '合规':
        return_str = 'The images are not pornographic'

    return_str = 'Image review results: '+return_str

    return return_str



if __name__ == '__main__':
    image_path = "images.jpg"
    result = final_ocr2(image_path)
    print(result)
