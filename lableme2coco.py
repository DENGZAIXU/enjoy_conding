# lableme 标注?rect 格式的json 文件 转化?Coco格式的可训练json 文件
# 把所有的 json文件整合为一个json

import argparse
import json
import matplotlib.pyplot as plt
import skimage.io as io
import cv2
#from labelme import utils
#
from image import img_b64_to_arr   #image.py是自己创建的py文件
#
import numpy as np
import glob
import PIL.Image
import PIL.ImageDraw
import pysnooper

#pysnooper.snoop()
class labelme2coco(object):
    def __init__(self,labelme_json=[],save_json_path='./new.json'):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列
        :param save_json_path: json保存位置
        '''
        self.labelme_json=labelme_json
        self.save_json_path=save_json_path
        self.images=[]
        self.categories=[
            {
                "supercategory": "Pepsi_Salt_Caramel",
                "id": 1,
                "name": "Pepsi_Salt_Caramel"
            },
            {
                "supercategory": "Taoti_Tea_Tea",
                "id": 2,
                "name": "Taoti_Tea_Tea"
            },
            {
                "supercategory": "Sprite_Fiber_Cucumber",
                "id": 3,
                "name": "Sprite_Fiber_Cucumber"
            },
            {
                "supercategory": "Ice_Tea",
                "id": 4,
                "name": "Ice_Tea"
            },
            {
                "supercategory": "Watsons_Soda",
                "id": 5,
                "name": "Watsons_Soda"
            },
            {
                "supercategory": "Ovaltine_Oat_Malt_Milk",
                "id": 6,
                "name": "Ovaltine_Oat_Malt_Milk"
            },
            {
                "supercategory": "Vitamin_Blue",
                "id": 7,
                "name": "Vitamin_Blue"
            },
            {
                "supercategory": "Vitasoy_Chocolate_Soymilk",
                "id": 8,
                "name": "Vitasoy_Chocolate_Soymilk"
            },
            {
                "supercategory": "Nestle",
                "id": 9,
                "name": "Nestle"
            },
            {
                "supercategory": "Hot_Kid",
                "id": 10,
                "name": "Hot_Kid"
            },
            {
                "supercategory": "Pepsi_Max",
                "id": 11,
                "name": "Pepsi_Max"
            },
            {
                "supercategory": "Perrier_Mineral_Water",
                "id": 12,
                "name": "Perrier_Mineral_Water"
            },
            {
                "supercategory": "NongFu_Leaf_Tea",
                "id": 13,
                "name": "NongFu_Leaf_Tea"
            },
            {
                "supercategory": "Sea_Salt_Lemon",
                "id": 14,
                "name": "Sea_Salt_Lemon"
            },
            {
                "supercategory": "Yuanqi_Shenlin_Peach_Soda",
                "id": 15,
                "name": "Yuanqi_Shenlin_Peach_Soda"
            },
            {
                "supercategory": "Monster_Mango",
                "id": 16,
                "name": "Monster_Mango"
            },
            {
                "supercategory": "Mizone_Peach",
                "id": 17,
                "name": "Mizone_Peach"
            },
            {
                "supercategory": "Xicha_Hawthorn_Tea",
                "id": 18,
                "name": "Xicha_Hawthorn_Tea"
            },
            {
                "supercategory": "Taoti_Green_Tea",
                "id": 19,
                "name": "Taoti_Green_Tea"
            },
            {
                "supercategory": "Mengniu_Fruit_Aloe",
                "id": 20,
                "name": "Mengniu_Fruit_Aloe"
            },
            {
                "supercategory": "Monster",
                "id": 21,
                "name": "Monster"
            },
            {
                "supercategory": "Vitaco_Coconut",
                "id": 22,
                "name": "Vitaco_Coconut"
            },
            {
                "supercategory": "Lussotto_Sugarless_Coffee",
                "id": 23,
                "name": "Lussotto_Sugarless_Coffee"
            },
            {
                "supercategory": "Amushi_Blueberry_Yogurt",
                "id": 24,
                "name": "Amushi_Blueberry_Yogurt"
            },
            {
                "supercategory": "Arctic_Orange_Soda",
                "id": 25,
                "name": "Arctic_Orange_Soda"
            },
            {
                "supercategory": "Vitamin_Orange",
                "id": 26,
                "name": "Vitamin_Orange"
            },
            {
                "supercategory": "Red_Bull_Enhanced",
                "id": 27,
                "name": "Red_Bull_Enhanced"
            },
            {
                "supercategory": "Yili_Fruit_Milkshake",
                "id": 28,
                "name": "Yili_Fruit_Milkshake"
            }
    ]
        self.annotations=[]
        # self.data_coco = {}
        self.label=["Pepsi_Salt_Caramel","Taoti_Tea_Tea","Sprite_Fiber_Cucumber",
                    "Ice_Tea","Watsons_Soda","Ovaltine_Oat_Malt_Milk",
                    "Vitamin_Blue","Vitasoy_Chocolate_Soymilk","Nestle",
                    "Hot_Kid","Pepsi_Max","Perrier_Mineral_Water",
                    "NongFu_Leaf_Tea","Sea_Salt_Lemon","Yuanqi_Shenlin_Peach_Soda",
                    "Monster_Mango","Mizone_Peach","Xicha_Hawthorn_Tea",
                    "Taoti_Green_Tea","Mengniu_Fruit_Aloe","Monster",
                    "Vitaco_Coconut","Lussotto_Sugarless_Coffee","Amushi_Blueberry_Yogurt",
                    "Arctic_Orange_Soda","Vitamin_Orange","Red_Bull_Enhanced",
                    "Yili_Fruit_Milkshake",]  ## 28 categories
        self.annID=1
        self.height=0
        self.width=0

        self.save_json()

    def data_transfer(self):
        for num,json_file in enumerate(self.labelme_json):
            with open(json_file,'r') as fp:
                data = json.load(fp)  
                self.images.append(self.image(data,num))
                for shapes in data['shapes']:
                    label=shapes['label']
                    ## label format：car （without supercategory imformation�?

                    # 添加 label 类
                    # if label not in self.label:
                    #     self.categories.append(self.categorie(label))
                    #     self.label.append(label)


                    ## label format: vehicle_car (with supercategory imformation�?
                    # label=shapes['label'].split('_')
                    # if label[1] not in self.label:
                    #     self.categories.append(self.categorie(label))
                    #     self.label.append(label[1])
                    points=shapes['points']
                    self.annotations.append(self.annotation(points,label,num))
                    self.annID+=1

    def image(self,data,num):
        image={}
        #img = img_b64_to_arr(data['imageData'])  # 解析原图片数�?
        height = data["imageHeight"]
        width = data["imageWidth"]
        img = None
        image['height']=height

        image['width'] = width
        image['id']= int(num+1)
        image['file_name'] = data['imagePath'].split('/')[-1]

        self.height=height
        self.width=width

        return image

    def categorie(self,label):
        categorie={}
        # categorie['supercategory'] = label[0]
        # categorie['id']=len(self.label)+1 #  default : 0 represents background
        # categorie['name'] = label[1]
        categorie['supercategory'] = label
        categorie['id']= int(len(self.label)+1) #  default : 0 represents background
        categorie['name'] = label

        return categorie

    def annotation(self,points,label,num):
        annotation={}
        #由点形成segmentation
        #annotation['segmentation']=[list(np.asarray(points).flatten())]
        annotation['iscrowd'] = 0
        annotation['image_id'] = int(num+1)

        annotation['bbox'] = list(map(float,self.getbbox(points)))

        #由bbox形成segmentation
        x =  annotation['bbox'][0]
        y =  annotation['bbox'][1]
        w =  annotation['bbox'][2]
        h =  annotation['bbox'][3]
        annotation['segmentation']=[[x,y,x+w,y,x+w,y+h,x,y+h]]

        annotation['category_id'] = self.getcatid(label)
        annotation['id'] = int(self.annID)
        #add area info
        annotation['area'] = self.height * self.width  # 这里用了原图的长和宽，并不是bbox的面积；但对检测任务不影响
        return annotation

    def getcatid(self,label):
        for categorie in self.categories:
            if label==categorie['name']:
                return categorie['id']
            # if label[1]==categorie['name']:
            #     return categorie['id']
        return -1

    def getbbox(self,points):
        # img = np.zeros([self.height,self.width],np.uint8)
        # cv2.polylines(img, [np.asarray(points)], True, 1, lineType=cv2.LINE_AA)  # 画边界线
        # cv2.fillPoly(img, [np.asarray(points)], 1)  # 画多边形 内部像素值为1
        polygons = points
        mask = self.polygons_to_mask([self.height,self.width], polygons)
        return self.mask2box(mask)

    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0�?组成的图�?
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        # return [(left_top_r,left_top_c),(right_bottom_r,right_bottom_c)]
        # return [(left_top_c, left_top_r), (right_bottom_c, right_bottom_r)]
        # return [left_top_c, left_top_r, right_bottom_c, right_bottom_r]  # [x1,y1,x2,y2]
        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def polygons_to_mask(self,img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco={}
        data_coco['images']=self.images
        data_coco['categories']=self.categories
        data_coco['annotations']=self.annotations
        return data_coco

    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()
        # 保存json文件
        json.dump(self.data_coco, open(self.save_json_path, 'w', encoding='utf-8'), indent=4, separators=(',', ': '), cls=MyEncoder)
 
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

# you need to modify the  path ָannotation.json
labelme_json=glob.glob('/data/DENGZAIXU/dataset/28_category_0814/annotation/*.json')
# /data/DENGZAIXU/dataset/28_category_0802
labelme2coco(labelme_json,'/data/DENGZAIXU//dataset/28_category_0814/train.json')
