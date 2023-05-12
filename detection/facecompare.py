import os, dlib, glob, numpy
import cv2
import dlib
import face_recognition
from skimage import io
import matplotlib.pyplot as plt
from PIL import Image

# 用于判度一张图片中所含人脸的数量
def facenumber(path):
    test_image = face_recognition.load_image_file(path)
    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
    face = face_recognition.face_locations(test_image)
    l = len(face)
    return l;

# 人脸关键点检测器
predictor_path = "dat/shape_predictor_68_face_landmarks.dat"
# 人脸识别模型、提取特征值
face_rec_model_path = "dat/dlib_face_recognition_resnet_model_v1.dat"
# 训练图像文件夹
faces_folder_path = 'candidates'

# 加载模型
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

candidate = []     #存放训练集任务名字
descriptors = []   #存放训练集人物特征列表

for f in glob.glob(os.path.join(faces_folder_path,"*.jpg")):
    img = io.imread(f)
    candidate.append(f.split('\\')[-1].split('.')[0])
    #人脸检测
    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = sp(img, d)
        #提取特征
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        v = numpy.array(face_descriptor)
        descriptors.append(v)

def face_familiar(path):
    img = io.imread(path)
    dets = detector(img, 1)
    dist = []
    for k, d in enumerate(dets):
        shape =sp(img, d)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        d_test = numpy.array(face_descriptor)
        for i in descriptors: # 计算距离
            dist_ = numpy.linalg.norm(i - d_test)
            dist.append(dist_)

    # 训练集人物和距离组成一个字典,并对字典进行排序
    c_d = dict(zip(candidate, dist))
    cd_sorted = sorted(c_d.items(), key=lambda d: d[1])

    # 获得最近（相似）的距离数据并与已知数据进行比较
    distance = c_d.get(cd_sorted[0][0])

    result1 = ''
    if distance > 0.48:
        result1 = "This image does not contain portrait of government officials"
    else:
        result1 = "This picture contains portrait of government officials. It is illegal！"

    return result1
