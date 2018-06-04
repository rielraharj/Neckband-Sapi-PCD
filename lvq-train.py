import numpy as np
import csv
from random import seed
from math import sqrt

##LVQ
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

# iterasi
def train_codebooks(train, n_codebooks, lrate, epochs):
    for epoch in range(epochs):
        rate = lrate * (1.0 - (epoch / float(epochs)))
        sum_error = 0.0
        for row in train:
            bmu = get_best_matching_unit(codebooks, row)
            for i in range(len(row) - 1):
                error = row[i] - bmu[i]
                sum_error += error ** 2
                if bmu[-1] == row[-1]:
                    bmu[i] += rate * error
                else:
                    bmu[i] -= rate * error
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, rate, sum_error))
        # print(codebooks)
    return codebooks

weight = "initial-weight.csv"


csvfile = "datavector.csv"

codebooks=[]
with open(weight, "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        # print ('line[{}] = {}'.format(i, line))
        a = []
        for x in line:
            a.append(int(x))
        codebooks.append(list(a))
print (codebooks)

vectorzone = []
with open(csvfile, "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        # print ('line[{}] = {}'.format(i, line))
        a = []
        for x in line[2:]:
            a.append(int(x))
        vectorzone.append(list(a))
print(vectorzone)
# Test the training function
seed(1)
dataset = vectorzone[2:]
learn_rate = 0.05
n_epochs = 150
n_codebooks = 8

codebooks=train_codebooks(dataset, n_codebooks, learn_rate, n_epochs)
np.savetxt("weight.csv", codebooks, delimiter=",")
print('Codebooks: %s' % codebooks)