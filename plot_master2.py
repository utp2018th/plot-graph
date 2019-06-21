import matplotlib.pyplot as plt
import math
import numpy as np
import csv
import sys
from scipy.optimize import curve_fit

# sig_dig : significant digit(有効数字)
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
    rc = [np.random.randint(0,255) for _ in range(3)]
    ans = '#{:02X}{:02X}{:02X}'.format(*rc)
    return ans

# フィッテイング曲線の種類
fitting_types = (
    'proportion',
    'liner',
    'Michaelis Menten'
    )

def mm(x,a,b):
    return  a*x/(b+x)

class Data:
    # それぞれのデータ行をオブジェクトとするためのクラス
    def __init__(self,l):
        self.label = l[0]
        self.values = np.array([float(i) for i in l[1:]])
        self.color = generate_random_color()
        self.sig_dig = 3 # デフォルトの有効数字
        self.fit_type = None
        self.fit_values = None

    def fitting(self,x):
        if self.fit_type == fitting_types[0]:
            self.fit_values = np.dot(x, self.values)/(x**2).sum()
        elif self.fit_type == fitting_types[1]:
            self.fit_values = np.polyfit(x,self.values,1)
        elif self.fit_type == fitting_types[2]:
            self.fit_values,cov = curve_fit(mm,x,self.values)

class Graph_master:
    # グラフの描画に関するクラスはこちら
    def __init__(self,args):
        for i,x in enumerate(args):
            if x == "":
                args[i] = 'You should input some words' if i < 3 else 'image'
        self.title = args[0]
        self.xlabel = args[1]
        self.ylabel = args[2]
        self.output_path = 'output/' + args[3]

    def plot_fitting(self,x,y):
        y.fitting(x.values)
        if y.fit_type == fitting_types[0]:
            a = y.fit_values
            y1 = a * x.values
            equation = 'y=' + str(round(a,y.sig_dig)) + 'x'
            corr = 'R={}'.format(round(np.corrcoef(x.values,y.values)[0][1],y.sig_dig))
            text = equation + '\n' + corr
            plt.plot(x.values,y1,c=y.color,label=text)

        elif y.fit_type == fitting_types[1]:
            a,b = y.fit_values
            y1 = a * x.values + b
            equation = 'y=' + str(round(a,y.sig_dig)) + 'x+' + str(round(b,y.sig_dig))
            corr = 'R={}'.format(round(np.corrcoef(x.values,y.values)[0][1],y.sig_dig))
            text = equation + '\n' + corr
            plt.plot(x.values,y1,c=y.color,label=text)

        elif y.fit_type == fitting_types[2]:
            a,b = y.fit_values
            x_line = np.linspace(min(x.values),max(x.values),100)
            y_line = a * x_line / (b + x_line)
            y1 = a * x.values / (b + x.values)
            equation = 'y={}x/({}+x)'.format(round(a,y.sig_dig),round(b,y.sig_dig))
            corr = np.corrcoef(y.values,y1)[0,1]
            equation_r = 'R={}'.format(round(corr,y.sig_dig))
            text = equation + '\n' + equation_r
            plt.plot(x_line,y_line,c=y.color,label=text)

        else:
            print("No Approximate Curve")

    def make_graph(self,var_x,ys):
        plt.figure(figsize=(9,6),dpi=128)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # 散布図と近似曲線のプロット
        input_text = 'もし比例の近似直線が欲しいなら1を、線形の近似直線が欲しいなら2を、'
        input_text += '近似直線が不要な場合はそれ以外の入力をしてください\n>> '
        ans = input(input_text)
        for var_y in ys:
            plt.scatter(var_x.values,var_y.values,label=var_y.label,c=var_y.color)
            if ans ==  "1":
                var_y.fit_type = fitting_types[0]
            elif ans == "2":
                var_y.fit_type = fitting_types[1]
            elif ans == "3":
                var_y.fit_type = fitting_types[2]
            self.plot_fitting(var_x,var_y)

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
        args = array2[0]
        del array2[0]
    else:
        title = input('グラフのタイトルを入力してください(なるべく英語で)\n>>')
        xlabel = input('x軸のラベルを入力してください(なるべく英語で)\n>>')
        ylabel = input('y軸のラベルを入力してください(なるべく英語で)\n>>')
        output_path = input('出力するファイル名を入力してください(なるべく英語で)\n>>')
        args = [title,xlabel,ylabel,output_path]

    # データをオブジェクト化した上でプロット
    box = []
    for idx,array in enumerate(array2):
        rows = Data(array)
        if idx == 0:
            x = rows
        else:
            box.append(rows)
    graph = Graph_master(args)
    graph.make_graph(x,box)

    # 直線の式をcsvに出力する
    with open(args[3]+'eq&R.csv',mode='w') as f:
        for i,y in enumerate(box):
            f.write('label,a,b\n')
            text0 = ""
            for i in y.fit_values:
                text0 += ',' + str(i)
            text = '{}{}\n'.format(y.label,text0)
            f.write(text)

if __name__ == "__main__":
    main(sys.argv)
