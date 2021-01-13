import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from shutil import copyfile

classes = ["head"]

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('wowTest/%s.xml'%image_id)
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls in classes:
            out_file = open('wowYoloLabel/%s.txt'%image_id, 'w')
            break

    for obj in root.iter('object'):
        cls = obj.find('name').text
        print("cls:",cls)
        if cls not in classes:
            continue
        person_cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        person_b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        #print("person person_b:",person_b)
        person_bb = convert((w,h), person_b)
        out_file.write(str(person_cls_id) + " " + " ".join([str(a) for a in person_bb]) + '\n')

wd = getcwd()

if not os.path.exists('wowYoloLabel/'):
    os.makedirs('wowYoloLabel/')
image_ids = open('train.txt').read().strip().split()

# imgCnt = 0
# pre_image_id = ""
# correct_image_ids = []
# for check_image_id in image_ids:
#     if len(check_image_id)<3:
#         continue
#     if check_image_id == pre_image_id:
#         continue
#     imgCnt+=1
#     #print(imgCnt)
#     #print(check_image_id)
#     correct_image_ids.append(check_image_id)
#     pre_image_id = check_image_id


# list_file = open('trainList.txt', 'w')
for image_id in image_ids:
    # list_file.write('wowTest/%s.jpg\n'%image_id)
    print("image_id:",image_id)
    # convert_annotation(image_id)
    if os.path.exists(r'.\label_depth_result\%s.png'%image_id):
        if os.path.exists(r'.\wowYoloLabel\%s.txt'%image_id):
            copyfile(r'.\label_depth_result\%s.png'%image_id, 'train_img/%s.png'%image_id)
            copyfile(r'.\wowYoloLabel\%s.txt'%image_id, 'train_label/%s.txt'%image_id)

# list_file.close()

#os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
#os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")

