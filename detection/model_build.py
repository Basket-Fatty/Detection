import glob
import os
import cv2
import tensorflow as tf
from tensorflow.python.keras import layers,optimizers
from sklearn.model_selection import train_test_split
import numpy as np

path = "./photos/"
w = 128
h = 128
c = 3

#2.2 导入实验数据集
# 步骤一 构建读取图片数据集函数
def read_img(path):
# 定义函数 read_img，用于读取图像数据，并且对图像进行 resize 格式统一处理
    cate=[path+x for x in os.listdir(path) if os.path.isdir(path+x)]
# 创建层级列表 cate，用于对数据存放目录下面的数据文件夹进行遍历，os.path.isdir 用于判断文件是否是目录，然后对是目录文件的文件进行遍历
    imgs=[]
# 创建保存图像的空列表
    labels=[]

# 创建用于保存图像标签的空列表
    for idx,folder in enumerate(cate):
    # enumerate 函数用于将一个可遍历的数据对象组合为一个索引序列，同时列出数据和下标,一般用在 for循环当中
        for im in glob.glob(folder+'/*.jpg'):
        # 利用 glob.glob 函数搜索每个层级文件下面符合特定格式“/*.jpg”进行遍历
            print('reading the images:%s'%(im))
        # 遍历图像的同时，打印每张图片的“路径+名称”信息
            img = cv2.imread(im)
        # 利用 cv2.imread 函数读取每一张被遍历的图像并将其赋值给 img
            img = cv2.resize(img, (w, h))
        # 利用 cv2.resize 函数对每张 img 图像进行大小缩放，统一处理为大小为 w*h(即 100*100)的图像
            imgs.append(img)
        # 将每张经过处理的图像数据保存在之前创建的 imgs 空列表当中
            labels.append(idx)
        # 将每张经过处理的图像的标签数据保存在之前创建的 labels 列表当中
    return np.asarray(imgs,np.float32),np.asarray(labels,np.int32)
    # 利用 np.asarray 函数对生成的 imgs 和 labels 列表数据进行转化，之后转化成数组数据（imgs 转成浮点数型，labels 转成整数型）
    # 最后返回 imgs 和 labels 数组数据

#步骤2 读取图片数据集
# 加载数据集
# 将 read_img 函数处理之后的数据定义为样本数据 data 和标签数据 label
data,label=read_img(path)
print(label)
print("shape of data:",data.shape) # 查看样本数据的大小
print("shape of label:",label.shape) # 查看标签数据的大小


#划分训练集与测试集
# 保证生成的随机数具有可预测性,即相同的种子（seed 值）所产生的随机数是相同的
seed = 785
np.random.seed(seed)
#切分数据集
(x_train, x_val, y_train, y_val) = train_test_split(data, label,
test_size=0.20, random_state=seed)
x_train = x_train / 255
x_val = x_val / 255
#创建图像标签列表
dict = {0:'emblem of China', 1:'flag of China', 2:'party emblem', 3:'cross',
               4:'gambling chip', 5:'gambling wheel', 6:'gun', 7:'nazi sign', 8:'taiji'}

model = tf.keras.models.Sequential([
    # 调用 layer.Con2D()创建了一个卷积层。32 表示 kernel 的数量。padding=“same”表示填充输入以使输出具有与原始输入相同的长度，使用 RELU 函数
    layers.Conv2D(input_shape=(128, 128, 3), filters=32, kernel_size=[5, 5], padding="same",
                  activation=tf.nn.relu),
    # 调用 layers.MaxPool2D()创建最大池化层，步长为 2，padding=“same”表示填充输入以使输出具有与原始输入相同的长度。
    layers.MaxPooling2D(pool_size=[2, 2], strides=2, padding='same'),
    # 利用 dropout 随机丢弃 25%的神经元
    layers.Dropout(0.25),
    # 继续添加两个卷积层和一个最大池化层
    layers.Conv2D(64, kernel_size=[3, 3], padding="same",
                  activation=tf.nn.relu),
    layers.Conv2D(64, kernel_size=[3, 3], padding="same",
                  activation=tf.nn.relu),
    layers.MaxPooling2D(pool_size=[2, 2], strides=2, padding='same'),
    layers.Dropout(0.25),
    # 继续添加两个卷积层和一个最大池化层
    layers.Conv2D(128, kernel_size=[3, 3], padding="same",
                  activation=tf.nn.relu),
    layers.MaxPooling2D(pool_size=[2, 2], strides=2, padding='same'),
    # 利用 dropout 随机丢弃 25%的神经元
    layers.Dropout(0.25),
    # Flatten 层用来将输入“压平”，即把多维的输入一维化
    layers.Flatten(),
    # 调用 layers.Dense()创建全连接层
    layers.Dense(512, activation=tf.nn.relu),
    layers.Dense(256, activation=tf.nn.relu),
    # 添加全连接层，最后输出每个分类（9）的数值
    layers.Dense(9, activation='softmax'),
])
# 步骤 2 构建优化器
#使用 Adam 优化器，优化模型参数。lr(learning_rate, 学习率)
opt = optimizers.Adam(lr=0.0001)
# 编译模型
# 定义准确率函数，用于模型效果验证。
#编译模型以供训练。metrics=['accuracy']即评估模型在训练和测试时的性能的指标。
model.compile(optimizer=opt,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

# 步骤 3 训练 CNN 图像识别模型
#训练模型，决定训练集和验证集，batch size：进行梯度下降时每个 batch 包含的样本数。
#verbose：日志显示，0 为不在标准输出流输出日志信息，1 为输出进度条记录，2 为每个 epoch 输出一行记录
model.fit(x_train, y_train, epochs=40, validation_data=(x_val,y_val),batch_size=100, verbose=1)
#输出模型的结构和参数量
model.summary()
model.save('./Model/model.h5')