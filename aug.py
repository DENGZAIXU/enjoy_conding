# - *-coding=utf-8 -*-
import cv2
import math
import numpy as np
import os
import pdb
import xml.etree.ElementTree as ET


class ImgAugemention():
    def __init__(self):
        self.angle = 90

    # rotate_img
    def rotate_image(self, src, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        # convet angle into rad
        rangle = np.deg2rad(angle)  # angle in radians
        # calculate new image width and height
        nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
        nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # map
        return cv2.warpAffine(
            src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))),
            flags=cv2.INTER_LANCZOS4)

    def rotate_xml(self, src, xmin, ymin, xmax, ymax, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        rangle = np.deg2rad(angle)  # angle in radians
        # now calculate new image width and height
        # get width and heigh of changed image
        nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
        nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # rot_mat: the final rot matrix
        # get the four center of edges in the initial martix，and convert the coord
        point1 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymin, 1]))
        point2 = np.dot(rot_mat, np.array([xmax, (ymin+ymax)/2, 1]))
        point3 = np.dot(rot_mat, np.array([(xmin+xmax)/2, ymax, 1]))
        point4 = np.dot(rot_mat, np.array([xmin, (ymin+ymax)/2, 1]))
        # concat np.array
        concat = np.vstack((point1, point2, point3, point4))
        # change type
        concat = concat.astype(np.int32)
        print(concat)
        rx, ry, rw, rh = cv2.boundingRect(concat)
        return rx, ry, rw, rh,angle

    def process_img(self, imgs_path, xmls_path, img_save_path, xml_save_path, angle_list):
        # assign the rot angles
        for angle in angle_list:
            for img_name in os.listdir(imgs_path):
                # split filename and suffix
                n, s = os.path.splitext(img_name)
                # for the sake of use yol model, only process '.jpg'
                if s == ".png" or s == '.jpeg':
                    img_path = os.path.join(imgs_path, img_name)
                    img = cv2.imread(img_path)
                    wa = img.shape[1]
                    ha = img.shape[0]
                    rotated_img = self.rotate_image(img, angle)
                    # 写入图像
                    cv2.imwrite(img_save_path + n + "_" + str(angle) + "d.png", rotated_img)
                    fname = n + "_" + str(angle) + "d.png" 
                    print("log: [%sd] %s is processed." % (angle, img))
                    xml_url = img_name.split('.')[0] +'.xml'
                    #+'.' + img_name.split('.')[1] 
                    xml_path = os.path.join(xmls_path, xml_url)
                    tree = ET.parse(xml_path)
                    root = tree.getroot()
                    for pname in root.iter('annotation'):
                        pname.find('filename').text = str(fname) 
                    for box in root.iter('bndbox'):
                        xmin = float(box.find('xmin').text)
                        ymin = float(box.find('ymin').text)
                        xmax = float(box.find('xmax').text)
                        ymax = float(box.find('ymax').text)
                        x, y, w, h, angle = self.rotate_xml(img, xmin, ymin, xmax, ymax, angle)
                        # change the coord
                        box.find('xmin').text = str(x)
                        box.find('ymin').text = str(y)
                        box.find('xmax').text = str(x+w)
                        box.find('ymax').text = str(y+h)
                        box.set('updated', 'yes')
                        for pose in root.iter('size'):
                            if angle == 90 or angle == 270:
                                pose.find('width').text = str(ha)
                                pose.find('height').text = str(wa)
                            if angle == 180:
                                pose.find('width').text = str(wa)
                                pose.find('height').text = str(ha)                                
                    # write into new xml
                    tree.write(xml_save_path + n + "_" + str(angle) + "d.xml")
                print("[%s] %s is processed." % (angle, img_name))


if __name__ == '__main__':
    img_aug = ImgAugemention()
    imgs_path = './pics'
    xmls_path = './xmls'
    img_save_path = './rotate/'
    xml_save_path = './xml_rot/'
    angle_list = [90,180,270,360]
    img_aug.process_img(imgs_path, xmls_path, img_save_path, xml_save_path, angle_list)
