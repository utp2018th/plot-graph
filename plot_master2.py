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
    input_mode = input('csv â†’ c tsv â†’ t else â†’ text \n>> ')
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
        self.sig_dig = 3 # デフォルトの有効数字
        self.proportion = None
        self.linear = None

    def get_proportion(self,x,y):
        self.proportion = np.dot(x, y)/(x**2).sum()

    def get_linear(self,x,y):
        self.linear = np.polyfit(x,y,1)

class graph_master:
    def __init__(self):
        self.xlabel = 'xlabel'
        self.ylabel = 'ylabel'
        self.title = 'Graph Title'

    def plot_proportion(self,x,y):
        if not y.proportion:
            y.get_proportion(x.values,y.values)
        a = y.proportion
        y1 = a * x.values
        label = 'y=' + str(round(a,4)) + 'x+'
        plt.plot(x.values,y1,c=y.color,label=)

    def make_graph(self,var_x,*var_y):
        plt.figure(figsize=(9,6),dpi=128)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        for y in var_y:
            plt.scatter(var_x.values,y.values,label=y.label,color=y.color)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=9)
        plt.subplots_adjust(right=0.77)
        plt.grid()

def test(a,*b):
    print(a)
    for i in b:
        print(i)
    print(b)

if __name__ == "__main__":
    path = 'input/0620.csv'
    get_array_from_data(path)
    test(1,2,3,4,5)
