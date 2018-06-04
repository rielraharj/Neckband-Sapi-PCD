import cv2
import numpy as np
import os
import glob
import csv
from math import sqrt

##jarak euclide
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


##ngecek yg terbaik
def get_best_matching_unit(codebooks, test_row):
    distances = list()
    for codebook in codebooks:
        dist = euclidean_distance(codebook, test_row)
        distances.append((codebook, dist))
    distances.sort(key=lambda tup: tup[1])
    return distances[0][0]

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

        im_gray = cv2.imread(image_path,0)
        thresh = 127
        im_binerr = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
        im_gray = cv2.medianBlur(im_gray,5)
        im_biner = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)

        print(neck_class)
        kelas = "Kelas "+str(neck_class)

        hasilarr = []
        arr = []
        v = []
        # if(neck_class==7):
        #     houghparam=35
        # else:
        #     houghparam=55

        try:
            houghparam = 55
            circles = cv2.HoughCircles(im_gray, cv2.HOUGH_GRADIENT, 1, 100, param1=290, param2=houghparam, minRadius=0, maxRadius=0)
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(im_biner, (i[0], i[1]), i[2], (0, 255, 255), 2)
                cv2.circle(im_biner, (i[0], i[1]), 2, (0, 0, 255), 112)
        except Exception:
            try:
                houghparam = 35
                circles = cv2.HoughCircles(im_gray, cv2.HOUGH_GRADIENT, 1, 100, param1=290, param2=houghparam, minRadius=0,
                                           maxRadius=0)
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    cv2.circle(im_biner, (i[0], i[1]), i[2], (0, 255, 255), 2)
                    cv2.circle(im_biner, (i[0], i[1]), 2, (0, 0, 255), 112)
            except Exception:
                sumclass[0]=sumclass[0]+1
                pass

        try:
            flag = 1
            row, col, ch = im_biner.shape
            graykanvas = np.zeros((row, col, 1), np.uint8)
            for i in range(0, row):
                for j in range(0, col):
                    b, g, r = im_biner[i, j]
                    if (b == 255 & g == 0 & r == 0):
                        graykanvas.itemset((i, j, 0), 255)
                        if (flag == 1):
                            x = i
                            y = j
                            flag = 100
                    else:
                        graykanvas.itemset((i, j, 0), 0)

            im_hasil = cv2.subtract(graykanvas, im_gray)

            hasil_crop = im_hasil[x:x + 112, y - 56:y + 56]  # im awe [y,x]
            thresh = 130

            kernel = np.ones((5, 5), np.uint8)

            crop_biner = cv2.threshold(hasil_crop, thresh, 255, cv2.THRESH_BINARY)[1]
            cv2.imwrite("test-asht.bmp",crop_biner)
            # cv2.imshow("test",crop_biner)



            cv2.imwrite(os.path.join(new_save_path,name),crop_biner)

            row, col= crop_biner.shape
            for r in range(0,row):
                a = 0
                for c in range(0,col):
                    if crop_biner[r,c]==255:
                        crop_biner[r,c]=1
                    a+=crop_biner[r,c]
                v.append(a)
            #     print(v)
            # print(r)
            print(len(v))
            print("tipe",type(v))
            print(v)
            v=v/max(v)
            v=[int(round(l)) for l in v]
            if (sum(v[:56]) < sum(v[56:])):
                v = v[::-1]

            # arr.append(nameimg)
            for d in v:
                arr.append(d)

            print(arr)


            hasil = get_best_matching_unit(codebooks, arr)
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
            sumclass[0] = sumclass[0] + 1
            pass


# cv2.imshow('test', crop_biner)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

accur = count_true/count_total

print(" ")
print("Jumlah testing benar = ", count_true)
print("Total testing dilakukan= ",count_total)
print("Accuracy = ", accur)
print(" ")
print("Jumlah total gambar = ", jumlahgambar)
print("Total gambar error = ",sumclass[0])

iter_testing += 1

filesummary = open("summary-testing.txt","a")
filesummary.write("====== TESTING KE-"+str(iter_testing)+" ======\n")
filesummary.write("Total gambar testing = "+ str(jumlahgambar)+"\n")
filesummary.write("Total gambar error = "+str(sumclass[0])+"\n")
filesummary.write("Jumlah testing benar = "+str(count_true)+"\n")
filesummary.write("Total testing dilakukan= "+str(count_total)+"\n")
filesummary.write("Accuracy = "+str(accur)+"\n")
filesummary.write("\n")
filesummary.close()



filejumlah=open("jumlah-testing.txt","w")
filejumlah.write(str(iter_testing))
filejumlah.close()