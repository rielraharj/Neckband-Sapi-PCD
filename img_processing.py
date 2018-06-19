import numpy as np
import cv2

def pattern_extract(image_path,houghparam):
    im_gray = cv2.imread(image_path, 0)
    # thresh = 127
    # im_binerr = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1] // Mungkin bisa diapus
    im_gray = cv2.medianBlur(im_gray, 5)
    im_biner = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)


    # if (neck_class == 7):
    #     houghparam = 35
    # else:
    #     houghparam = 55

    try:

        circles = cv2.HoughCircles(im_gray, cv2.HOUGH_GRADIENT, 1, 100, param1=290, param2=houghparam, minRadius=0,
                                   maxRadius=0)
        circles = np.uint16(np.around(circles))
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


        # kernel = np.ones((5, 5), np.uint8)

        crop_biner = cv2.threshold(hasil_crop, thresh, 255, cv2.THRESH_BINARY)[1]
        return crop_biner
    except Exception:
        pass


def vector_extract(source_image):
    v = []
    row, col = source_image.shape
    for r in range(0, row):
        a = 0
        for c in range(0, col):
            if source_image[r, c] == 255:
                source_image[r, c] = 1
            a += source_image[r, c]
        v.append(a)
    # print(v)
    # print(r)
    # print(len(v))
    # print("tipe", type(v))
    # print(v)
    v = v / max(v)
    v = [int(round(l)) for l in v]
    if (sum(v[:56]) < sum(v[56:])):
        v = v[::-1]
    return v