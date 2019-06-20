import matplotlib.pyplot as plt
import math
import numpy as np
import csv

def sig_dig(float):
    plus = True
    if float < 0:
        plus = False
    pass

def get_array_from_data(path):
    input_mode = input('csv c tsv  t else text \n>> ')
    with open(path) as f:
        if input_mode == "c":
            reader = csv.reader(f)
        elif input_mode == "t":
            reader = csv.reader(f,delimiter = '\t')
        else:
            reader = [s.strip() for s in f.readlines()]
        reader = [i for i in reader]
    print(reader)

def generate_random_color():
    return '#{:X}{:X}{:X}'.format(*[random.randint(0, 255) for _ in range(3)])

class Data:
    def __init__(self,l):
        self.label = l[0]
        self.values = np.array([float(i) for i in l[1:]])
        self.color = generate_random_color()
        self.sig_dig = 3 #
