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

def main():
    path = get_file_name()
    data = get_array_from_xlsx(path)

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

    title = 'Title'
    xlabel = 'xlabel'
    ylabel = 'ylabel'
    output_path = 'day3/graph1'
    sig_dig = '4'
    args = [title,xlabel,ylabel,output_path,sig_dig]

    graph = pm2.Graph_master(args)
    graph.make_graph(x,box)
    plt.savefig(graph.output_path)

    for i in box:
        print(i.fit_values)



if __name__ == "__main__":
    main()
