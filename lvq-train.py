import numpy as np
import csv
from random import seed
from math import sqrt
import lvq

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

codebooks=lvq.train_codebooks(dataset, n_codebooks, learn_rate, n_epochs)
np.savetxt("weight.csv", codebooks, delimiter=",")
print('Codebooks: %s' % codebooks)