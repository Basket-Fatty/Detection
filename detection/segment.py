from PIL import Image
import sys


def cut_image(image):
    width_part = 1
    width, height = image.size
    height_part = int(height/width)+1
    item_width = int(width / width_part)
    item_height = int(height / height_part)


    box_list = []
    # (left, upper, right, lower)
    for i in range(0, height_part):
        for j in range(0, width_part):
            # print((j * item_width, i * item_height, (j + 1) * item_width, (i + 1) * item_height))
            box = (j * item_width, i * item_height, (j + 1) * item_width, (i + 1) * item_height)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]
    return image_list


# 保存
def save_images(image_list):
    index = 1
    for image in image_list:
        image.save('C:/Users/86134/PycharmProjects/Detection01/detection/long_photo_segmentation/' + str(index) + '.jpg', 'JPEG')
        index += 1

def image_size(path):
    file_path = path
    image = Image.open(file_path)
    if image.height > 10000:
        return 1
    else:
        return 0

def if_need_segment(path):
    file_path = path
    image = Image.open(file_path)
    if image.height > 10000:
        image_list = cut_image(image)
        save_images(image_list)
        root = 'C:/Users/86134/PycharmProjects/Detection01/detection/long_photo_segmentation/'
    else:
        root = path

    return root

'''
if __name__ == '__main__':
    #file_path = "C:/Users/10723/detection/data/3D蒸汽热敷眼罩.jpg"
    file_path = "C:/Users/86134/PycharmProjects/untitled1/photos/9.normal/39.jpg"

    image = Image.open(file_path)
    print(image.height)
    if image.height >10000 :
        image_list = cut_image(image)
        save_images(image_list)
    else:
        print("This is a small image")
'''
