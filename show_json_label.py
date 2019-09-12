import xml.dom.minidom
import cv2
import os
import json

def parse_json(json_path):
    if(os.path.exists(json_path)):
        with open(json_path) as f:
            data = json.load(f)
            coords = list()
            objs = data["shapes"]

            for idx, obj in enumerate(objs):
                label = objs[idx]["label"]
                xmin = int(obj["points"][0][0])
                ymin = int(obj["points"][0][1])
                xmax = int(obj["points"][1][0])
                ymax = int(obj["points"][1][1])
                coords.append([xmin, ymin, xmax, ymax, label])
            return coords

json_path ='/home/algoteam2/xu/mmdetection/imgs/Capture20190814104032173.json'

img_path = '/home/algoteam2/xu/mmdetection/imgs/Capture20190814104032173.jpg'

bbox = parse_json(json_path)

img = cv2.imread(img_path)


for i in range(len(bbox)):
    xmin = bbox[i][0]
    ymin = bbox[i][1]
    xmax = bbox[i][2]
    ymax= bbox[i][3]

    cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 3)  #依次将label画到图片上
save_path ='/home/algoteam2/xu/mmdetection/imgs/result000.jpg'

cv2.imwrite(save_path, img)
cv2.imshow("label", img)
cv2.waitKey(0)
