import cv2
import numpy as np
import os
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


image_path = input("Masukkan nama file : \n")



im_gray = cv2.imread(image_path,0)
thresh = 127
im_binerr = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
im_gray = cv2.medianBlur(im_gray,5)
im_biner = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)


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
        print("Error pola tidak terdeteksi")
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
    cv2.imshow("test",crop_biner)



    row, col= crop_biner.shape
    for r in range(0,row):
        a = 0
        for c in range(0,col):
            if crop_biner[r,c]==255:
                crop_biner[r,c]=1
            a+=crop_biner[r,c]
        v.append(a)

    # print(len(v))
    # print("tipe",type(v))
    # print(v)
    v=v/max(v)
    v=[int(round(l)) for l in v]
    if (sum(v[:56]) < sum(v[56:])):
        v = v[::-1]

    for d in v:
        arr.append(d)

    # print(arr)


    hasil = get_best_matching_unit(codebooks, arr)
    # print(codebooks)
    # print(arr[1:])
    print("Gambar diklasifikasikan ke dalam : ")
    if hasil[-1] == 1: print("Kelas 1")
    if hasil[-1] == 2: print("Kelas 2")
    if hasil[-1] == 3: print("Kelas 3")
    if hasil[-1] == 4: print("Kelas 4")
    if hasil[-1] == 5: print("Kelas 5")
    if hasil[-1] == 6: print("Kelas 6")
    if hasil[-1] == 7: print("Kelas 7")
    if hasil[-1] == 8: print("Kelas 8")


except Exception:
    print("Error pola tidak terdeteksi")
    pass


cv2.waitKey(0)
cv2.destroyAllWindows()

