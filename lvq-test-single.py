import cv2
import numpy as np
import os
from math import sqrt
import lvq
import img_processing as improc

codebooks = np.genfromtxt('weight.csv', delimiter=',')


image_path = input("Masukkan nama file : \n")

try:
    houghparam = 55
    crop_biner = improc.pattern_extract(image_path, houghparam)
except Exception:
    try:
        houghparam = 35
        crop_biner = improc.pattern_extract(image_path, houghparam)
    except Exception:
        pass

        # cv2.imwrite("test-asht.bmp",crop_biner)
        # cv2.imshow("test",crop_biner)

cv2.imshow("Hasil test", crop_biner)

try:
    v = improc.vector_extract(crop_biner)

    # arr.append(nameimg)
    arr = []
    for d in v:
        arr.append(d)

    # print(arr)


    hasil = lvq.get_best_matching_unit(codebooks, arr)
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

