import cv2
import numpy as np
import csv
#i=1

# file = open("datavector.csv","w")

for i in range(1,10):
    neck_class = 3
    print (i)
    x=str(i)
    print(x)
    print(type(x))
    name = x + "test.bmp"
    print(name)
    print(type(name))
    im_gray = cv2.imread(x+".bmp",0)
    #i += 1
    thresh = 127
    im_binerr = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("img binerr",im_binerr)
    im_gray = cv2.medianBlur(im_gray,5)
    # cv2.imshow("img medianblur",im_gray)

    im_biner = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(im_gray, cv2.HOUGH_GRADIENT,1,100,param1=290, param2=55,
                               minRadius=0, maxRadius=0)
    arr = []
    v = []
    try:
        circles = np.uint16(np.around(circles))
        # cv2.imshow("hasil", circles)
        for i in circles[0, :]:
            cv2.circle(im_biner, (i[0], i[1]), i[2], (0, 255, 255), 2)
            cv2.circle(im_biner, (i[0], i[1]), 2, (0, 0, 255), 112)

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

        cv2.imshow("hasil crop", hasil_crop)
        thresh = 130

        kernel = np.ones((5, 5), np.uint8)

        crop_biner = cv2.threshold(hasil_crop, thresh, 255, cv2.THRESH_BINARY)[1]
        #cv2.imshow("hasil circle crop biner", crop_biner)



        cv2.imwrite(name,crop_biner)
        # print("aaa")
        row, col= crop_biner.shape
        print(row,col)

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
        # max=max(v)
        v=v/max(v)
        v=[int(round(l)) for l in v]

        arr.append(name)
        for d in v:
            arr.append(d)
        arr.append(neck_class)
        print(arr)
        # wibu.append(arr[0])
        # for i in arr[1]:
        #     wibu.append(i)
        # wibu.append(arr[2])
        #
        # print(wibu)



        # arr_np = np.array(arr)
        csvfile = "datavector.csv"

        with open(csvfile, 'a+',newline='') as output:
            writer = csv.writer(output, lineterminator=',')
            for val in arr[:-1]:
                writer.writerow([val])
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow([arr[-1]])
        # csv.writer("vectorkalung")
        #
        # np.savetxt("datavectorkalung.csv",arr,delimiter=",")

        # img_dilation = cv2.dilate(crop_biner, kernel, iterations=1)
        # cv2.imshow("dilasi", img_dilation)
        # img_erosion = cv2.erode(img_dilation, kernel, iterations=1)
        # cv2.imshow("akhir", img_erosion)

    except Exception:
        pass

