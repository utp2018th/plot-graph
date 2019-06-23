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

def plot_and_save(args,x,y):
    import matplotlib.pyplot as plt
    import plot_master2 as pm2

    x = pm2.Data(x)
    y = ["v"] + list(y)
    y = pm2.Data(y)
    ys = [y]
    plt.ylim(min(y.values),max(y.values))
    graph = pm2.Graph_master(args)
    graph.make_graph(x,ys)
    plt.savefig(graph.output_path)
    data = Plot_data()
    for y in ys:
        data.v_max = y.fit_values[0]
        data.k_m = y.fit_values[1]
        data.k_cat = data.v_max / (4.0*10**-9)
        data.k2 = data.k_cat / data.k_m
    return data

def main():
    path = get_file_name()
    data = get_array_from_xlsx(path)

    import numpy as np
    import matplotlib.pyplot as plt
    import plot_master2 as pm2
    import sys

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
    output_path = 'day3/graph1'
    sig_dig = '4'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    # 吸光度の変化をプロットする
    graph = pm2.Graph_master(args)
    graph.make_graph(x,box)
    plt.savefig(graph.output_path)

    # 反応初速度を求める
    v0 = []
    for i in box:
        if i.fit_values.size == 1:
            v0.append(i.fit_values)
        else:
            v0.append(i.fit_values[0])
    v0 = np.array(v0)
    e492 = 85000*10**(-6)
    v0 /= e492

    # ６点でミカエリスメンテン
    # 変数の定義
    title = 'Michaelis Menten Plot (6 dots)'
    xlabel = 'Substrate concentration (μM)'
    ylabel = 'Reaction rate (M/sec)'
    output_path = 'day3/graph2'
    sig_dig = '4'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    # プロット
    data_array.append(plot_and_save(args,array_s,v0))

    # 4点でミカエリスメンテン
    # 変数の定義
    title = 'Michaelis Menten Plot (4 dots)'
    xlabel = 'Substrate concentration (μM)'
    ylabel = 'Reaction rate (M/sec)'
    output_path = 'day3/graph3'
    sig_dig = '4'
    args = [title,xlabel,ylabel,output_path,sig_dig]


    print("v0",v0)
    print("array_s",array_s)
    # プロット
    data_array.append(plot_and_save(args,array_s[:5],v0[:4]))


if __name__ == "__main__":
    main()
