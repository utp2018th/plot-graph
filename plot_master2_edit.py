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
    # グラフ化したい表のファイルを読み込んで、二重配列を返す
    input_mode = input('読み込むファイルが\ncsvなら「c」を、tsvなら「t」を、どちらでもない場合はそれ以外を入力してください\n>> ')
    with open(path) as f:
        if input_mode == "c":
            reader = csv.reader(f)
        elif input_mode == "t":
            reader = csv.reader(f,delimiter = '\t')
        else:
            reader = [s.strip() for s in f.readlines()]
        array2 = [Data(x) for x in reader]
    return array2

def generate_random_color():
    rc = [np.random.randint(0, 255) for _ in range(2)]
    rc += [max(0,255-sum(rc))]
    ans = '#{:02X}{:02X}{:02X}'.format(*rc)
    return ans

class Data:
    # それぞれのデータ行をオブジェクトとするためのクラス
    def __init__(self,l):
        self.label = l[0]
        self.values = np.array([float(i) for i in l[1:]])
        self.color = generate_random_color()
        self.sig_dig = 3 # デフォルトの有効数字
        self.proportion = None
        self.linear = None

    def get_proportion(self,x):
        self.proportion = np.dot(x.values, self.values)/(x.values**2).sum()

    def get_linear(self,x):
        self.linear = np.polyfit(x.values,self.values,1)


class Graph_master:
    # グラフの描画に関するクラスはこちら
    def __init__(self):
        self.xlabel = 'xlabel'
        self.ylabel = 'ylabel'
        self.title = 'Graph Title'
        self.output_path = 'output/sample'

    def plot_proportion(self,x,y):
        if not y.proportion:
            y.get_proportion(x)
        a = y.proportion
        y1 = a * x.values
        equation = 'y = {:.3e}x'.format(a)
        corr = 'R = {:.4}'.format(np.corrcoef(x.values,y.values)[0][1])
        text = equation + '\n' + corr
        plt.plot(x.values,y1,c=y.color,label=text)

    def plot_liner(self,x,y):
        if not y.linear:
            y.get_linear(x)
        a,b = y.linear
        y1 = a * x.values + b
        equation = 'y = {0:.3e}x + {1:.3e}'.format(a,b)
        corr = 'R = {:.4}'.format(np.corrcoef(x.values,y.values)[0][1])
        text = equation + '\n' + corr
        plt.plot(x.values,y1,c=y.color,label=text)

    def make_graph(self,var_x,ys):
        plt.figure(figsize=(9,6),dpi=128)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        input_text = 'もし比例の近似直線が欲しいなら1を、線形の近似直線が欲しいなら2を、'
        input_text += '近似直線が不要な場合はそれ以外の入力をしてください\n>> '
        ans = input(input_text)
        for var_y in ys:
            plt.scatter(var_x.values,var_y.values,label=var_y.label,c=var_y.color)
            if ans ==  "1":
                self.plot_proportion(var_x,var_y)
            elif ans == "2":
                self.plot_liner(var_x,vary)

        # グラフの外観をいい感じに調節しているのはここ
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=9)
        plt.subplots_adjust(right=0.77)
        plt.grid()
        msg = input('作成したグラフを保存するなら「s」を、画面に表示するならそれ以外の入力をしてください\n>> ')
        if msg == "s":
            plt.savefig(self.output_path)
        else:
            plt.show()

if __name__ == "__main__":
    path = 'input/sample.csv'
    array2 = get_array_from_data(path)
    x = array2[0]
    graph = Graph_master()
    graph.make_graph(x,array2[1:])
