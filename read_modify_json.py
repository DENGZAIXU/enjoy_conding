import json
import os
def modify_json(json_file):

    data = json.load(open(json_file,'rb'))
    # data["shapes"][0]["label"] = "Hot_Kid"
    # data["imageData"] = None
    data['imagePath'] = data['imagePath'].split('\\')[-1]
    with open(json_file, 'w') as f:
        json.dump(data, f,indent= 4)




def main():
    data_path = "/home/algoteam2/xu/dataset/validation/annotation"
    # image_path = os.path.join(data_path,"image")
    # ann_path = os.path.join(data_path,"annotation")
    all_ann = os.listdir(data_path)
    print(len(all_ann))
    for file_path in all_ann:
        if(file_path.endswith(".json")):
            modify_json(os.path.join(data_path,file_path))


if __name__ == '__main__':
    main()