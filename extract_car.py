#coding:utf-8
from pycocotools.coco import COCO
import os
import shutil
from tqdm import tqdm
import skimage.io as io
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw
import json

#the path you want to save your results for coco to voc
savepath="/home/gnss/cocoapi/PythonAPI/jieguo/"
img_dir=savepath+'imagesval/'
#anno_dir=savepath+'Annotations/'
# datasets_list=['train2014', 'val2014']
datasets_list=['val2014']

#classes_names = ['car','bus', 'truck']
classes_names = ['car']
#Store annotations and train2014/val2014/... in this folder
cocoDir = '/home/gnss/FCIS/data/coco'
dataDir= '/home/gnss/FCIS/data/coco/images/'

jsonfile_path = '/home/gnss/cocoapi/PythonAPI/jieguo/coco_car_val.json'
#if the dir is not exists,make it,else delete it
def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
mkr(img_dir)
#mkr(anno_dir)
def id2name(coco):
    classes=dict()
    for cls in coco.dataset['categories']:
        classes[cls['id']]=cls['name']
    return classes



def save_annotations_and_imgs(coco,dataset,filename):

    img_path=dataDir+dataset+'/'+filename
    print(img_path)
    dst_imgpath=img_dir+filename

    img=cv2.imread(img_path)

    shutil.copy(img_path, dst_imgpath)




for dataset in datasets_list:
    #./COCO/annotations/instances_train2014.json
    annFile='/home/gnss/FCIS/data/coco/annotations/instances_minival2014.json'

    #COCO API for initializing annotated data
    coco = COCO(annFile)

    #show all classes in coco

    classes = id2name(coco)
    print(classes)
    #[1, 2, 3, 4, 6, 8]
    #assert 1==0
    classes_ids = coco.getCatIds(catNms=classes_names)
    print(classes_ids)
    #assert 1==0

    #ann = coco["annotations"]
    #print ann
    #assert 1==0
    with open("/home/gnss/FCIS/data/coco/annotations/instances_minival2014.json","r+") as f:
        allData = json.load(f)
        data = allData["annotations"]
        cat = allData['categories']

        id = 3 #id for vehicle

        ann_dict = {}
        images = []
        annotations = []
        #message = dict


        car_list = []

        #image = {}
        
        for i in range(len(data)):
        
            if (id == data[i]['category_id']):
        
                car_list.append(data[i])

        img = allData['images']


        for i in range(len(img)):
        
            img_id = img[i]['id']

            for j in range(len(car_list)):

                if (img_id == car_list[j]['image_id']):
                #image = dict()

                    image = {}
                    #a = img[j].get('file_name')
                    #image["file_name"] = img[j].get('file_name')
                    image["id"] = img[i].get("id")
                    image["file_name"] = img[i].get("file_name")
                    image["height"] = img[i].get("height")
                    image["width"] = img[i].get("width")
                    #image["coco_url"] = img[j].get("coco_url")

                    images.append(image)

                    break

                    #print images
                    #assert 1==0            

        ann_dict['images'] = images
        #with open(jsonfile_path, 'w') as outfile:
        #    outfile.write(json.dumps(ann_dict))
        #assert 1==0


    for cls in classes_names:
        #Get ID number of this class
        cls_id=coco.getCatIds(catNms=[cls])
        img_ids=coco.getImgIds(catIds=cls_id)
        print(cls,len(img_ids)),2222
        # imgIds=img_ids[0:10]
        #annIds = coco.getAnnIds([id], catIds=cls_id, iscrowd=None)
        #anns = coco.loadAnns(annIds)

        for imgId in tqdm(img_ids):
            img = coco.loadImgs(imgId)[0]
            filename = img['file_name']
            # print(filename)
            #objs=showimg(coco, dataset, img, classes,classes_ids,show=False) 		###########

            annIds = coco.getAnnIds(imgId, catIds=cls_id, iscrowd=None)			######### [imgId]
            anns = coco.loadAnns(annIds)
            #print anns,11111111
            #assert 1==0

            #an = {}
            #an['id'] = anns[7]
            #an['image_id'] = anns[4]
            #an['segmentation'] = anns[1]
            #an['category_id'] = anns[6]
            #an['iscrowd'] = anns[3]
            #an['area'] = anns[2]
            #an['bbox'] = anns[5]

            #annotations.append(anns)
            for c in range(len(anns)):
                annotations.append(anns[c])



            #annotations.append(anns[0])

        ann_dict['annotations'] = annotations

        #categories = [{"id": category_dict[name], "name": name} for name in
        #              category_dict]

        categories = [{"supercategory": "vehicle", "id": 3, "name": "car"}]		################## id 

        ann_dict['categories'] = categories

        with open(jsonfile_path, 'w') as outfile:
            outfile.write(json.dumps(ann_dict))
        #assert 1==0






            #save_annotations_and_imgs(coco, dataset, filename)





