import matplotlib.pyplot as plt
import math
import numpy as np
import csv
import sys

def sig_dig(float):
    plus = True
    if float < 0:
        plus = False
    pass

def get_array_from_data(path):
    # グラフ化したい表のファイルを読み込んで、二重配列を返す
    input_mode = input('読み込むファイルが\ncsvなら「c」を、tsvなら「t」を、どちらでもない場合はそれ以外の入力してください\n>> ')
    with open(path) as f:
        if input_mode == "c":
            reader = csv.reader(f)
        elif input_mode == "t":
            reader = csv.reader(f,delimiter = '\t')
        else:
            reader = [s.strip() for s in f.readlines()]
        array2 = [i for i in reader]
    return array2

def generate_random_color():
    ans = ""
    while len(ans) != 7:
        ans = '#{:X}{:X}{:X}'.format(*[np.random.randint(0, 255) for _ in range(3)])
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

    def get_proportion(self,x,y):
        self.proportion = np.dot(x, y)/(x**2).sum()

    def get_linear(self,x,y):
        self.linear = np.polyfit(x,y,1)

class Graph_master:
    # グラフの描画に関するクラスはこちら
    def __init__(self,title='Graph Title',xlabel='xlabel',ylabel='ylabel',output_path='img'):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.output_path = 'output' + output_path

    def plot_proportion(self,x,y):
        if not y.proportion:
            y.get_proportion(x.values,y.values)
        a = y.proportion
        y1 = a * x.values
        equation = 'y=' + str(round(a,y.sig_dig)) + 'x'
        corr = 'R={}'.format(round(np.corrcoef(x.values,y.values)[0][1],y.sig_dig))
        text = equation + '\n' + corr
        plt.plot(x.values,y1,c=y.color,label=text)

    def plot_liner(self,x,y):
        if not y.linear:
            y.get_linear(x.values,y.values)
        a,b = y.linear
        y1 = a * x.values + b
        equation = 'y=' + str(round(a,y.sig_dig)) + 'x+' + str(round(b,y.sig_dig))
        corr = 'R={}'.format(round(np.corrcoef(x.values,y.values)[0][1],y.sig_dig))
        text = equation + '\n' + corr
        plt.plot(x.values,y1,c=y.color,label=text)

    def make_graph(self,var_x,var_y):
        plt.figure(figsize=(9,6),dpi=128)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        input_text = 'もし比例の近似直線が欲しいなら1を、線形の近似直線が欲しいなら2を、'
        input_text += '近似直線が不要な場合はそれ以外の入力をしてください\n>> '
        ans = input(input_text)
        for y in var_y:
            plt.scatter(var_x.values,y.values,label=y.label,c=y.color)
            if ans ==  "1":
                self.plot_proportion(var_x,y)
            elif ans == "2":
                self.plot_liner(var_x,y)

        # グラフの外観をいい感じに調節しているのはここ
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=9)
        plt.subplots_adjust(right=0.77)

        plt.grid()
        msg = input('作成したグラフを保存するなら「s」を、画面に表示するならそれ以外の入力をしてください\n>> ')
        if msg == "s":
            plt.savefig(self.output_path)
        else:
            plt.show()

def main(argv):
    # ファイル読み込み
    if len(argv) == 2:
        path = argv[1]
    else:
        path = input('グラフ化したい表のファイルを入力してください\n>> ')
    array2 = get_array_from_data(path)

    # 表の出力
    msg = input('読み込むファイルにあらかじめグラフのタイトルなどを入れている場合は「1」を、そうでない場合はそれ以外の入力をしてください\n>> ')
    if msg == "1" and len(array2[0]) == 4:
        title,xlabel,ylabel,output_path = array2[0]
        del array2[0]
    else:
        title = input('グラフのタイトルを入力してください(なるべく英語で)\n>>')
        xlabel = input('x軸のラベルを入力してください(なるべく英語で)\n>>')
        ylabel = input('y軸のラベルを入力してください(なるべく英語で)\n>>')
        output_path = input('出力するファイル名を入力してください(なるべく英語で)\n>>')

    # データをオブジェクト化した上でプロット
    box = []
    for idx,array in enumerate(array2):
        rows = Data(array)
        if idx == 0:
            x = rows
        else:
            box.append(rows)
    graph = Graph_master(title,xlabel,ylabel,output_path)
    graph.make_graph(x,box)

if __name__ == "__main__":
    main(sys.argv)
