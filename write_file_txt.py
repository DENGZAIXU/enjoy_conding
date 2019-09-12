from random import shuffle
import os
def ListFilesToTxt(dir,file,wildcard,recursion):
    exts = wildcard.split(" ")
    files = os.listdir(dir)
    for name in files:
        fullname=os.path.join(dir,name)
        if(os.path.isdir(fullname) & recursion):
            ListFilesToTxt(fullname,file,wildcard,recursion)
        else:
            for ext in exts:
                if(name.endswith(ext)):
                    (filename,extension) = os.path.splitext(name)
                    file.write(filename + " " + "depth/" + name + "\n")
                    break
def Test():
    file_dir="/data/DENGZAIXU/test/"
    outfile="/data/DENGZAIXU/good_test_list.txt"
    wildcard = ".png .txt .exe .dll .lib"
    
    goods_list = os.listdir(file_dir)
    for idx, good in enumerate(goods_list):
        
        good_path = os.path.join(file_dir , good)


        for i, file in enumerate (sorted(os.listdir(good_path))):
            name = good +'/' + file
            with open(outfile, 'a+') as f:
                f.write(name + '\n')



    
#    ListFilesToTxt(dir,file,wildcard, 1)
    
 #   file.close()
#Test()


def Pair():

    file_dir="/data/DENGZAIXU/dataset/arcface/dataset/train/"
    outfile="/data/DENGZAIXU//dataset/arcface/train_list.txt"
    wildcard = ".png .txt .exe .dll .lib"
    
    pair_list = []
    goods_list = os.listdir(file_dir)
    for idx, good in enumerate(goods_list):
        
        for pair in goods_list[idx:]:

            good_path = os.path.join(file_dir , good)
            pair_path = os.path.join(file_dir , pair)


            for i, file in enumerate (sorted(os.listdir(good_path))):
                for p in sorted(os.listdir(pair_path)):
                    if good == pair :
                        la = str(1)
                    else:
                        la = str(0)
                    name = good +'/' + file + ' ' + pair +'/' + p + ' ' + la
                    pair_list.append(name)

    shuffle(pair_list)
    with open(outfile, 'a+') as f:
        for name in pair_list[:10000] :
            f.write(name + '\n')



    
#    ListFilesToTxt(dir,file,wildcard, 1)
    
 #   file.close()
Pair()
