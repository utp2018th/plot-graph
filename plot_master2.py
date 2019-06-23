import matplotlib.pyplot as plt
import math
import numpy as np
import csv
import sys
from scipy.optimize import curve_fit


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
    'Michaelis Menten 6',
    'Michaelis Menten 4',
    )

def mm(x,a,b):
    return  a*x/(b+x)

class Data:
    # それぞれのデータ行をオブジェクトとするためのクラス
    def __init__(self,l):
        self.label = l[0]
        self.values = np.array([float(i) for i in l[1:]])
        self.color = generate_random_color()
        self.fit_type = None
        self.fit_values = None
        self.corr = None    # 相関係数
        self.r_sq = None    # 決定係数
        self.rss = None     # 残渣変動の二乗和

    def fitting(self,x):
        if self.fit_type == fitting_types[0]:
            self.fit_values = np.dot(x, self.values)/(x**2).sum()
        elif self.fit_type == fitting_types[1]:
            self.fit_values = np.polyfit(x,self.values,1)
        elif self.fit_type == fitting_types[2]:
            self.fit_values,cov = curve_fit(mm,x,self.values)
        elif self.fit_type == fitting_types[3]:
            self.fit_values,cov = curve_fit(mm,x[:4],self.values[:4])

class Graph_master:
    # グラフの描画に関するクラスはこちら
    def __init__(self,args):
        for i,x in enumerate(args):
            if x == "":
                if i < 3:
                    args[i] = 'You should input some words'
                elif i == 3:
                    args[i] = 'image'
            if i == 4 and x.isdecimal() == False:
                args[i] = 3
        self.title = args[0]
        self.xlabel = args[1]
        self.ylabel = args[2]
        self.output_path = 'output/' + args[3]
        self.sig_dig = int(args[4])

    def plot_fitting(self,x,y,max_x=None):
        y.fitting(x.values)

        if y.fit_type == fitting_types[0]:
            a = y.fit_values
            y1 = a * x.values
            pre_equation = 'y={:.' + str(self.sig_dig) + 'e}x'
            equation = pre_equation.format(a)
            y.corr = np.corrcoef(x.values,y.values)[0][1]
            y.r_sq = y.corr ** 2
            text_corr = 'R={:.4}'.format(round(y.corr,self.sig_dig))
            text = equation + '\n' + text_corr
            plt.plot(x.values,y1,c=y.color,label=text)

        elif y.fit_type == fitting_types[1]:
            a,b = y.fit_values
            y1 = a * x.values + b
            if b >= 0:
                pre_equation = 'y={:.' + str(self.sig_dig) + 'e}x+{:.' + str(self.sig_dig) + 'e}'
                equation = pre_equation.format(a,b)
            else:
                pre_equation = 'y={:.' + str(self.sig_dig) + 'e}x-{:.' + str(self.sig_dig) + 'e}'
                equation = pre_equation.format(a,abs(b))
            y.corr = np.corrcoef(x.values,y.values)[0][1]
            y.r_sq = y.corr ** 2

            # ここの２行はreplace_kaleida用
            residuals =  y.values - y1
            y.rss = np.sum(residuals**2)  #residual sum of squares = rss

            text_corr = 'R={:.4}'.format(round(y.corr,self.sig_dig))
            text = equation + '\n' + text_corr
            plt.plot(x.values,y1,c=y.color,label=text)

        elif y.fit_type in fitting_types[2:4]:
            a,b = y.fit_values
            if max_x:
                x_line = np.linspace(min(x.values),max_x,100)
            else:
                x_line = np.linspace(min(x.values),max(x.values),100)
            y_line = a * x_line / (b + x_line)
            y1 = a * x.values / (b + x.values)
            pre_equation = 'y={:.' + str(self.sig_dig) + 'e}x/({:.' + str(self.sig_dig) + 'e}+x)'
            equation = pre_equation.format(a,b)
            residuals =  y.values - mm(x.values,a,b)
            y.rss = np.sum(residuals**2)  #residual sum of squares = rss
            tss = np.sum((y.values - np.mean(y.values))**2) #total sum of squares = tss
            y.r_sq = 1 - (y.rss / tss)
            text_r_sq = 'R2={:.4}'.format(y.r_sq)
            text= equation + '\n' + text_r_sq
            plt.plot(x_line,y_line,c=y.color,label=text)

        else:
            print("No Approximate Curve")

    def make_graph(self,var_x,ys,input_mode=None,max_x=None):
        plt.figure(figsize=(9,6),dpi=128)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # 散布図と近似曲線のプロット
        if not input_mode:
            input_text = 'もし比例の近似直線が欲しいなら1を、線形の近似直線が欲しいなら2を、'
            input_text += 'ミカエリス・メンテン式の曲線で近似する場合は3を、'
            input_text += '近似直線が不要な場合はそれ以外の入力をしてください\n>> '
            input_mode = input(input_text)
        for var_y in ys:
            plt.scatter(var_x.values,var_y.values,label=var_y.label,c=var_y.color)
            if input_mode ==  "1":
                var_y.fit_type = fitting_types[0]
            elif input_mode == "2":
                var_y.fit_type = fitting_types[1]
            elif input_mode == "3":
                var_y.fit_type = fitting_types[2]
            elif input_mode == "4":
                var_y.fit_type = fitting_types[3]
            self.plot_fitting(var_x,var_y,max_x)

        # グラフの外観をいい感じに調節しているのはここ
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=9)
        plt.subplots_adjust(right=0.7)

        plt.grid()

    def output_graph(self):
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
    if msg == "1" and len(array2[0]) == 5:
        args = array2[0]
        del array2[0]
    else:
        title = input('グラフのタイトルを入力してください(なるべく英語で)\n>>')
        xlabel = input('x軸のラベルを入力してください(なるべく英語で)\n>>')
        ylabel = input('y軸のラベルを入力してください(なるべく英語で)\n>>')
        output_path = input('出力するファイル名を入力してください(なるべく英語で)\n>>')
        sig_dig = input('今回のグラフで扱う有効数字を入力してください\n>> ')
        args = [title,xlabel,ylabel,output_path,sig_dig]

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
    graph.output_graph()

    # 近似式と相関係数をcsvに出力する
    with open('output/'+args[3]+'-fitted.csv',mode='w') as f:
        f.write('label,a,b\n')
        for i,y in enumerate(box):
            text0 = ""
            if y.fit_values.size == 1:
                text0 = "," + str(y.fit_values)
            else:
                for i in y.fit_values:
                    text0 += ',' + str(i)
            text = '{}{}\n'.format(y.label,text0)
            f.write(text)

if __name__ == "__main__":
    main(sys.argv)
