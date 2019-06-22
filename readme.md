## plot_master について

このPythonプログラムを実行すればmatplotlibで綺麗なグラフが作れるよ。

>  ### 追記 2019/6/21
> `plot_master2` を作りました。そちらの方が最新のものになります。
> 以下の説明も`plot_master2`に対応したものです。

> ### 追記 2019/6/22
> ミカエリス・メンテン式に対応した近似曲線のプロットが可能になりました。

## 扱える表
csv形式とtsv形式に対応しています。
プロットするのに適しているのは、以下のようなものです。

1. 横軸が比率尺度あるいは間隔尺度となる数値(整数または小数)である。
2. 縦軸は横軸`x`に応じた数値`y`である。

例えば以下の表は３人の生徒の暗記時間とそれに応じたテストの点数を表しています。

|暗記時間|0|1.5|3|4.5|6|7.5|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|Ace|10|21|23|40|61|73|
|Jack|5|11|15|27|40|51|
|Roland|20|22|43|54|76|89|

これを`plot_master2.py`を使ってグラフ化すると以下のようになります。
なお、各サンプルのラベル(Ace)とかは英語にしておきましょう。日本語だとうまく出力されません。

![サンプル](https://github.com/utp2018th/plot-graph/blob/master/output/sample_with_title.png)

また、最小二乗法を用いた近似直線も引くことが可能です。説明については気が向いたら書きます。

## とりあえずの使い方
自分の使いたい環境にクローンしてください。
ターミナルなどで以下のように実行しましょう。

```
$ python plot_master2.py
```

あるいは以下のように入力したいファイル名を引数として入力することができます。

```
$ python plot_master2.py input/sample.csv
```

その後
```
読み込むファイルにあらかじめグラフのタイトルなどを入れている場合は「1」を、そうでない場合はそれ以外の入力をしてください
>>
```
という標準出力が返ってきます。
ここで「1」以外を入力すると、「グラフのタイトル」,「x軸のラベル」,「y軸のラベル」,「出力先のファイル名」、「有効数字」が問われるので、続けて入力してください。
何回もこれを手打ちするのは面倒かと思われるので、あらかじめグラフのタイトルなどを読み込むファイルに書いておくことで手間を省くことができます。
その際は [sample_with_title.csv](https://github.com/utp2018th/plot-graph/blob/master/input/sample_with_title.csv) のように、
１行目に「グラフのタイトル」,「x軸のラベル」,「y軸のラベル」,「出力先のファイル名」、「有効数字」をカンマ区切り(tsvの場合はタブ区切り)で入力しておきましょう。

まだまだ未完成な部分もありますが使いたい人はどうぞw
