import cv2
import numpy as np
import os
import glob
import csv
from math import sqrt
import lvq
import img_processing as improc
import confusion_matrix as cm



codebooks = np.genfromtxt('weight.csv', delimiter=',')

count_true = 0
count_total = 0

sumclass=[0,0,0,0,0,0,0,0,0]
save_path_pola = "pola testing"

jumlahgambar=0

filejumlah=open("jumlah-testing.txt","r")
iter_testing = filejumlah.read()
iter_testing = int(iter_testing)
print(iter_testing)
filejumlah.close()

##TESTING DARI FOLDER##
for class_image_path in glob.glob("D:\PycharmProjects\PCDSAPI\gambar testing\*"):
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

    class_folder = "Kelas " + str(neck_class)
    new_save_path = os.path.join(save_path_pola, class_folder)

    for image_path in glob.glob(os.path.join(class_image_path, "*.bmp")):
        print(image_path)
#######################

################# ngambil gambar
# nameimg="buattest8.bmp"
        x = str(neck_class) + "-class-" + str(sumclass[neck_class])
        name = x + "-hasil_test.bmp"

        jumlahgambar=jumlahgambar+1

        try:
            houghparam = 55
            crop_biner = improc.pattern_extract(image_path, houghparam)
        except Exception:
            try:
                houghparam=35
                crop_biner = improc.pattern_extract(image_path, houghparam)
            except Exception:
                pass

            # cv2.imwrite("test-asht.bmp",crop_biner)
            # cv2.imshow("test",crop_biner)



        cv2.imwrite(os.path.join(new_save_path,name),crop_biner)

        try:
            v = improc.vector_extract(crop_biner)

            # arr.append(nameimg)
            arr = []
            for d in v:
                arr.append(d)

            print(arr)


            hasil = lvq.get_best_matching_unit(codebooks, arr)
            print(codebooks)
            print(arr[1:])
            if hasil[-1] == 1: print("Kelas 1")
            if hasil[-1] == 2: print("Kelas 2")
            if hasil[-1] == 3: print("Kelas 3")
            if hasil[-1] == 4: print("Kelas 4")
            if hasil[-1] == 5: print("Kelas 5")
            if hasil[-1] == 6: print("Kelas 6")
            if hasil[-1] == 7: print("Kelas 7")
            if hasil[-1] == 8: print("Kelas 8")

            if hasil[-1] == neck_class:
                count_true+=1
            count_total+=1

            hasilarr = []
            hasilarr.append(name)
            hasilarr.append(image_path.split("\\")[-1])
            hasilarr.append(hasil[-1])
            hasilarr.append(neck_class)

            csvfile = "hasiltest.csv"

            with open(csvfile, 'a', newline='') as output:
                writer = csv.writer(output, lineterminator=',')
                for val in hasilarr[:-1]:
                    writer.writerow([val])
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow([hasilarr[-1]])

            sumclass[neck_class] = sumclass[neck_class] + 1

        except Exception:
            pass




# cv2.imshow('test', crop_biner)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cm.create_confusion_matrix(csvfile)

accur = count_true/count_total

print(" ")
print("Jumlah testing benar = ", count_true)
print("Total testing dilakukan= ",count_total)
print("Accuracy = ", accur)
print(" ")
print("Jumlah total gambar = ", jumlahgambar)
count_error = jumlahgambar-count_total
print("Total gambar error = ",count_error)

iter_testing += 1

filesummary = open("summary-testing.txt","a")
filesummary.write("====== TESTING KE-"+str(iter_testing)+" ======\n")
filesummary.write("Total gambar testing = "+ str(jumlahgambar)+"\n")
filesummary.write("Total gambar error = "+str(count_error)+"\n")
filesummary.write("Jumlah testing benar = "+str(count_true)+"\n")
filesummary.write("Total testing dilakukan= "+str(count_total)+"\n")
filesummary.write("Accuracy = "+str(accur)+"\n")
filesummary.write("\n")
filesummary.close()



filejumlah=open("jumlah-testing.txt","w")
filejumlah.write(str(iter_testing))
filejumlah.close()