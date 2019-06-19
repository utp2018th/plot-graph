import matplotlib.pyplot as plt
import math
import numpy as np


class Plot_master():
    # Textmasterのデータ→リストと同じ
    def read_text_as_list(self,path):
        with open(path) as f:
            l = [s.strip() for s in f.readlines()] #2行あけるようにしている
        return l

    # csvを二重配列に直す
    def csv_lists_to_array(self,path):
        array = self.read_text_as_list(path)
        for s in range(len(array)):
            array[s] = [i for i in array[s].split(",")]
        return array

    def lr_1(self,x,y):
        x = np.array(x)
        y = np.array(y)
        a = np.dot(x, y)/(x**2).sum()
        return a

    def plot_lr_1(self,x,y):
        # y=ax の近似直線を引く
        # 参考 https://qiita.com/takubb/items/9e3c207b381c3bdd0787
         a = self.lr_1(x, y)
         y1 = a * x
         plt.plot(x, y1, c='#566bd4')
         plt.text(0,0.02, 'y='+ str(round(a,4)) +'x')
         corr = round(np.corrcoef(x,y)[0][1],5)
         plt.text(50,0.02,"R = {}".format(corr))

    def plot_polyfit(self,x,y):
        # y=ax+b の近似直線を引く
        # 相関係数 Correlation coefficient
        a,b = np.polyfit(x,y,1)
        y2 = a * x + b
        plt.plot(x,y2,color='#2860aa')
        plt.text(x[0]+15,b, 'y='+ str(round(a,8)) +'x+'+str(round(b,8)))
        corr = round(np.corrcoef(x,y)[0][1],5)
        plt.text(100,b,"R = {}".format(corr))

    def make_graph1(self,array):
        """
        以下の形のグラフをプロットする

        |   |x_1|x_2|...|x_n|
        |ex1| y | y |   | y |
        |ex2| y | y |   | y |
        |ex3| y | y |   | y |
        """
        xlabel = 'x-label'
        ylabel = 'y-label'
        box = []
        labels =[]
        for i,row in enumerate(array):
            if i == 0:
                x_line = [float(i) for i in row[1:]]
            else:
                labels.append(row[0])
                box.append([float(i) for i in row[1:]])
        x_line = np.array(x_line)

        print("box",box)
        print("labels",labels)

        for i,y in enumerate(box):
            plt.scatter(x_line,y,label=labels[i])
            input_text = 'もし比例の近似直線が欲しいなら1を、線形の近似直線が欲しいなら2を、'
            input_text += '近似直線が不要な場合はそれ以外の入力をしてください\n>> '
            ans = input(input_text)
            if ans ==  "1":
                self.plot_lr_1(x_line,y)
            elif ans == "2":
                self.plot_polyfit(x_line,y)

        plt.title('Graph title')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=9)
        plt.subplots_adjust(right=0.77)
        # plt.subplots_adjust(right=0.8)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # グリッド線を引く
        plt.grid()
        # それぞれの軸の最大値と最小値
        plt.xlim(-10)
        plt.ylim(0)

if __name__ == "__main__":
    plt.figure(figsize=(3*3,2*3),dpi=128)
    path = 'input/sample.csv'
    data = Plot_master()
    data = data.csv_lists_to_array(path)
    pm = Plot_master()
    pm.make_graph1(data)
    txt = input('1 → save, else → show\n>> ')
    if txt == "1":
        plt.savefig("output/graph")
    else:
        plt.show()
