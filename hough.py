import cv2
import numpy as np
import csv
import glob
import os
import img_processing as improc

sumclass=[0,0,0,0,0,0,0,0,0]
save_path_pola = "pola kalung"

#Mengambil gambar tiap folder kelas
for class_image_path in glob.glob("D:\PycharmProjects\PCDSAPI\kalung sapi\*"):
    print(class_image_path)
    if (class_image_path.split("\\")[-1] == 'Kelas 1'): neck_class = 1
    if (class_image_path.split("\\")[-1] == 'Kelas 2'): neck_class = 2
    if (class_image_path.split("\\")[-1] == 'Kelas 3'): neck_class = 3
    if (class_image_path.split("\\")[-1] == 'Kelas 4'): neck_class = 4
    if (class_image_path.split("\\")[-1] == 'Kelas 5'): neck_class = 5
    if (class_image_path.split("\\")[-1] == 'Kelas 6'): neck_class = 6
    if (class_image_path.split("\\")[-1] == 'Kelas 7'): neck_class = 7
    if (class_image_path.split("\\")[-1] == 'Kelas 8'): neck_class = 8
    f = True
    class_folder = "Kelas "+str(neck_class)
    new_save_path = os.path.join(save_path_pola,class_folder)
    print("PATH ==",new_save_path)
    for image_path in glob.glob(os.path.join(class_image_path, "*.bmp")):
        print(image_path)
        # if(neck_class!=7):
        #     break
        x=str(neck_class)+"-class-"+str(sumclass[neck_class])
        name = x + "-test.bmp"
        print(name)
        print(type(name))

        if(neck_class==7):
            houghparam=35
        else:
            houghparam=55
        try:
            crop_biner = improc.pattern_extract(image_path,houghparam)
        except Exception:
            pass

        cv2.imwrite(os.path.join(new_save_path,name),crop_biner)

        try:
            v = improc.vector_extract(crop_biner)
        except Exception:
            pass
        arr=[]
        arr.append(name)
        arr.append(image_path.split("\\")[-1])
        for d in v:
            arr.append(d)
        arr.append(neck_class)
        print(arr)


        csvfile = "datavector.csv"

        with open(csvfile, 'a+',newline='') as output:
            writer = csv.writer(output, lineterminator=',')
            for val in arr[:-1]:
                writer.writerow([val])
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([arr[-1]])

        sumclass[neck_class]=sumclass[neck_class]+1



        if (sumclass[neck_class]==50):
            break
