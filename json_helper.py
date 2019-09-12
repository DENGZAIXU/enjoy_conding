import json
import os


def parse_json(json_path):
    if(os.path.exists(json_path)):
        with open(json_path) as f:
            data = json.load(f)
            coords = list()
            objs = data["shapes"]

            for idx, obj in enumerate(objs):
                label = obj[idx]["label"]
                xmin = int(obj[idx]["points"][0][0])
                ymin = int(obj[idx][0]["points"][0][1])
                xmax = int(obj[idx][0]["points"][1][0])
                ymax = int(obj[idx][0]["points"][1][1])
                coords.append([xmin, ymin, xmax, ymax, label])
            return coords


def generate_json(img_name,coords,img_size,out_root_path):
    '''
    输入：
        img_name：图片名称，如a.jpg
        coords:坐标list，格式为[[x_min, y_min, x_max, y_max, name]]，name为概况的标注
        img_size：图像的大小,格式为[h,w,c]
        out_root_path: xml文件输出的根路径

    '''
    new_data = {}
    new_data["version"] = "3.16.1"
    new_data["flags"] = {}
    new_data["shapes"] = []
    new_data["lineColor"] = [0, 255, 0, 128]
    new_data["fillColor"] = [255, 255, 0, 64]

    new_data["imagePath"] = img_name
    new_data["imageData"] = None
    new_data["imageWidth"] = img_size[1]
    new_data["imageHeight"] = img_size[0]


    for coor in coords:
        cont = {}
        cont["label"] = coor[4]
        cont["line_color"] = None
        cont["fill_color"] = None
        cont["points"] = [[coor[0], coor[1]], [coor[2] ,coor[3]]]
        cont["shape_type"] = "rectangle"
        cont["flags"] = {}
        new_data["shapes"].append(cont)

    with open(out_root_path, 'w+') as f:
        json.dump(new_data, f, indent=4)



