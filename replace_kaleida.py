def get_file_name():
    import os, tkinter, tkinter.filedialog, tkinter.messagebox

    root = tkinter.Tk()
    root.withdraw()
    # 選択候補を拡張子xlsxに絞る
    filetype = [("", "*.xlsx")]
    dirpath = os.path.abspath(os.path.dirname(".{}input{}".format(os.sep,os.sep)))
    tkinter.messagebox.showinfo('ファイル選択', '分析するエクセルファイルを選択してください')
    # 選択したファイルのパスを取得
    filepath = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = dirpath)
    return filepath

def get_array_from_xlsx(path):
    import openpyxl as px

    wb = px.load_workbook(path)
    sheet = wb.active
    data = []
    for rows in sheet.iter_rows(min_row=1, min_col=1, max_row=sheet.max_row, max_col=sheet.max_column):
        array = []
        for cell in rows:
            array.append(cell.value)
        data.append(array)
    return data

class Plot_data:
    def __init__(self):
        self.v_max = None
        self.k_cat = None
        self.k_m = None
        self.k2 = None
        self.rss = None

    def calc(self):
        self.k_cat = self.v_max / (4.0 * 10**(-9))
        self.k2 = self.k_cat / self.k_m

def main():
    path = get_file_name()
    data = get_array_from_xlsx(path)

    import numpy as np
    import matplotlib.pyplot as plt
    import plot_master2 as pm2
    import sys
    import csv

    box = []
    array_s = []
    for idx,row in enumerate(data):
        array_s.append(row[1])
        del row[1]
        array = pm2.Data(row)
        if idx == 0:
            x = array
        else:
            box.append(array)

    data_array = []

    # 吸光度のプロットに必要な変数
    title = 'Absorbance to Time'
    xlabel = 'Time(sec)'
    ylabel = 'Absorbance'
    output_path = 'day3/Absorbance'
    sig_dig = '3'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    # 吸光度の変化をプロットする
    graph = pm2.Graph_master(args)
    graph.make_graph(x,box,input_mode="2")
    plt.savefig(graph.output_path)

    # 反応初速度を求める
    v0 = []
    for i in box:
        if i.fit_values.size == 1:
            v0.append(i.fit_values)
        else:
            v0.append(i.fit_values[0])
    v0 = np.array(v0)
    e492 = 85000*10**(-6) # 勝手に10^-6倍してる
    v0 /= e492

    # ６点でミカエリスメンテン
    # 変数の定義
    title = 'Michaelis Menten Plot (6 dots)'
    xlabel = 'Substrate concentration (μM)'
    ylabel = 'Reaction rate (M/sec)'
    output_path = 'day3/MichaelisMenten6'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    # プロット
    x = pm2.Data(array_s)
    y = ["v"] + list(v0)
    y = pm2.Data(y)
    ys = [y]
    plt.ylim(min(y.values),max(y.values))
    graph = pm2.Graph_master(args)
    graph.make_graph(x,ys,input_mode="3",max_x=500)
    plt.savefig(graph.output_path)
    data = Plot_data()
    for y in ys:
        data.v_max = y.fit_values[0]
        data.k_m = y.fit_values[1]
        data.rss = y.rss
        data.calc()
    data_array.append(data)

    # 4点でミカエリスメンテン
    # 変数の定義
    title = 'Michaelis Menten Plot (4 dots)'
    xlabel = 'Substrate concentration (μM)'
    ylabel = 'Reaction rate (M/sec)'
    output_path = 'day3/MichaelisMenten4'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    # プロット
    x = pm2.Data(array_s[:5])
    y = ["v"] + list(v0[:4])
    y = pm2.Data(y)
    ys = [y]
    plt.ylim(min(y.values),max(y.values))
    graph = pm2.Graph_master(args)
    graph.make_graph(x,ys,input_mode="4",max_x=500)
    plt.savefig(graph.output_path)
    data = Plot_data()
    for y in ys:
        data.v_max = y.fit_values[0]
        data.k_m = y.fit_values[1]
        data.rss = y.rss
        data.calc()
    data_array.append(data)

    # Lineweaver-Burk Plot
    # 下準備
    var_x = np.array(array_s[1:])
    var_x = 1 / var_x
    var_y = 1 / v0

    # 変数の定義
    title = 'Lineweaver-Burk Plot'
    xlabel = '1 / Substrate concentration (/μM)'
    ylabel = '1 / Reaction rate (sec/M)'
    output_path = 'day3/Lineweaver-Burk'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    # プロット
    var_x = [array_s[0]] + list(var_x)
    x = pm2.Data(var_x)
    y = ["v"] + list(var_y)
    y = pm2.Data(y)
    ys = [y]
    plt.ylim(min(y.values),max(y.values))
    graph = pm2.Graph_master(args)
    graph.make_graph(x,ys,input_mode="2",max_x=500)
    plt.savefig(graph.output_path)
    data = Plot_data()
    for y in ys:
        data.v_max = 1 / y.fit_values[1]
        data.k_m = y.fit_values[0] / y.fit_values[1]
        data.rss = y.rss
        data.calc()
    data_array.append(data)

    # Eadie-Hofstee Plot
    # 下準備
    s = np.array(array_s[1:])
    var_y = v0
    var_x = v0 / s

    # 変数の定義
    title = 'Eadie-Hofstee Plot'
    xlabel = 'Reaction rate / Substrate concentration'
    ylabel = 'Reaction rate (M/sec)'
    output_path = 'day3/Eadie-Hofstee'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    # プロット
    var_x = [array_s[0]] + list(var_x)
    x = pm2.Data(var_x)
    y = ["v"] + list(var_y)
    y = pm2.Data(y)
    ys = [y]
    plt.xlim(min(x.values),max(x.values))
    graph = pm2.Graph_master(args)
    graph.make_graph(x,ys,input_mode="2")
    plt.savefig(graph.output_path)
    data = Plot_data()
    for y in ys:
        data.v_max = y.fit_values[1]
        data.k_m = - y.fit_values[0]
        data.rss = y.rss
        data.calc()
    data_array.append(data)

    with open('output/day3/compare-k.csv',mode='w') as f:
        f.write(',M-M,6M-M,4L-B,E-H\n')
        k_cat = ",".join([i.k_cat for i in data_array])
        f.write(k_cat+'\n')
        k_m = ",".join([i.k_m for i in data_array])
        f.write(k_m+'\n')
        k2 = ",".join([i.k2 for i in data_array])
        f.write(k2+'\n')
        rss = ",".join([i.rss for i in data_array])
        f.write(rss+'\n')


if __name__ == "__main__":
    main()
