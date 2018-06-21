import csv
import numpy as np

def create_confusion_matrix(filename):
    conf_matrix = np.zeros(shape=(8,8))
    csvfile = filename

    with open(csvfile, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            x = int(line[2])
            y = int(line[3])
            conf_matrix[x-1][y-1]+=1
    print(conf_matrix)


# create_confusion_matrix("test2.csv")
