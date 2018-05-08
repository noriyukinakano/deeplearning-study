# 前処理　第1章〜pandaの操作〜

## 準備
対象データのダウンロードをおこないましょう。
今回はテストデータとして、顧客を想定したusers.csvと顧客が購入した注文を想定したorders.csvを用意しました。

### users.csv
| id | name | name_yomi | email | gender | age | birthday | marriage | pref | tel | mobile | communication_carrier | created_at | last_login_in_at | deleted_at |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |  :-- |  :-- |  :-- |  :-- |  :-- |  :-- |  :-- |
1 | 菅澤 菜々美 | すがさわ ななみ | sugasawa_nanami@example.com | 女 | 24 | 1994/4/3 | 既婚 | 福岡県 | 076-574-8128 | 080-5780-6228 | au | 2016/04/02 20:04:14 | 2017/06/23 22:57:56 | |
2 | 早美 寿明 | はやみ としあき | hayami_toshiaki@example.com | 男 | 81 | 1936/5/6 | 既婚 | 京都府 | 030-360-3241 | 080-7765-4316 | ソフトバンク | 2016/04/03 4:58:21 | 2017/06/22 12:58:26 | 2018/04/17 23:52:26 |
3 | 小高 美咲 | こだか みさき | kodaka_misaki@example.com | 女 | 83 | 1934/9/12 | 既婚 | 石川県 | 097-756-3099 | 080-2275- 338 | ドコモ | 2016/04/03 8:06:23 | 2017/06/04 6:26:15 |  |

```bash
cd /usr/local/src/
wget "https://drive.google.com/uc?export=download&id=1VIJ5u_wQCmn8Pc30DTTIWbB8mv8WYAHN" -O users.csv
```


### orders.csv
| id | user_id | product | price | ordered_at |
| :-- | :-- | :-- | :-- | :-- |
| 103 | 53 | Beer - Upper Canada Lager | 2905 | 2017/04/24 4:52:06 |
| 104 | 304 | Muffin - Blueberry Individual | 9035 | 2017/04/24 6:58:14 |
| 105 | 176 | Tart Shells - Sweet 4 | 5884 | 2017/04/24 23:22:45 |

```bash
cd /usr/local/src/
wget "https://drive.google.com/uc?export=download&id=1tojnXWV3wI8tNMSTQukr6Mrxg1wps4IJ" -O orders.csv
```

## PandasでのCSV読み込み
用意してあるDockerイメージを用いて、対話式pythonで学習しましょう。
Dockerイメージのコンテナにはディスプレイを接続していないため
おまじないとして固定の環境変数を設定し、対話モードでpythonを起動させます。

```bash
env DISPLAY=:0 PYTHONIOENCODING=utf-8 MPLBACKEND="agg" python3.6
```

### pandasのライブラリインポート

```python3
>>> # coding:utf-8
>>> from __future__ import print_function, division
>>>
>>> import os.path
>>> import sys
>>> import pandas as pd
>>> import seaborn
>>> import numpy as np
>>> import matplotlib as mpl
>>> mpl.use('Agg')
```

### CSVデータの読み込み

対話式のpythonに入ると「>>> 」と表示されます。
以下の「>>> 」の横に書いてあるのが実行するコマンドです。
まずはpandasでcsvをインポートしてみましょう。

```python3
>>> users_original_df = pd.read_csv('/usr/local/src/users.csv')
>>> users_original_df

      id    name   name_yomi                           email gender   age  \
0      1  菅澤 菜々美    すがさわ ななみ     sugasawa_nanami@example.com      女  24.0
1      2   早美 寿明    はやみ としあき     hayami_toshiaki@example.com      男  81.0
2      3   小高 美咲     こだか みさき       kodaka_misaki@example.com      女  83.0
..   ...     ...         ...                             ...    ...   ...
497  498   岸田 光臣    きしだ みつおみ    kishida_mitsuomi@example.com      男  72.0
498  499   松沢 良介  まつざわ りょうすけ  matsuzawa_ryousuke@example.com      男  37.0
499  500   野村 みあ      のむら みあ          nomura_mia@example.com      女  83.0

        birthday marriage  pref           tel         mobile  \
0      1994/4/3       既婚   福岡県  076-574-8128  080-5780-6228
1      1936/5/6       既婚   京都府  030-360-3241  080-7765-4316
2     1934/9/12       既婚   石川県  097-756-3099  080-2275- 338
..   ...     ...         ...                             ...    ...   ...
497    1945/5/3       既婚   新潟県  058-827-3883  080-9625-6055
498   1981/3/17       未婚   東京都  066-868-8519  080-4870- 646
499   1934/8/16       既婚   埼玉県  089-700-4330  090-6190-7332

    communication_carrier           created_at     last_login_in_at  \
0                      au  2016/04/02 20:04:14  2017/06/23 22:57:56
1                  ソフトバンク   2016/04/03 4:58:21  2017/06/22 12:58:26
2                     ドコモ   2016/04/03 8:06:23   2017/06/04 6:26:15
..   ...     ...         ...                             ...    ...   ...
497                   ドコモ   2017/07/06 7:30:34  2017/08/29 20:53:06
498                ソフトバンク  2017/07/06 12:04:24  2017/08/16 20:00:33
499                    au   2017/07/07 5:11:38   2017/07/08 2:28:34

deleted_at
0                    NaN
1    2018/04/17 23:52:26
2                    NaN
..   ...
497   2017/11/01 8:55:57
498                  NaN
499                  NaN

[500 rows x 15 columns]

>>> orders_original_df = pd.read_csv('/usr/local/src/orders.csv')



       id  user_id                           product  price  \
0     103       53         Beer - Upper Canada Lager   2905
1     104      304     Muffin - Blueberry Individual   9035
2     105      176            Tart Shells - Sweet, 4   5884
..    ...      ...                               ...    ...
997    10       52                    Ginger - Fresh   5614
998   230      467           Rum - Mount Gay Eclipes   1723
999    86      351                     Glaze - Clear   2877

      ordered_at
0     2017/04/24 4:52:06
1     2017/04/24 6:58:14
2    2017/04/24 23:22:45
..                   ...
998  2017/06/05 11:07:07
999   2017/02/16 4:00:22

[1000 rows x 5 columns]
```

pandasではcsvの元の列に加え、indexという概念が存在します。
通常何も指定しないでCSVを読み込みを行うと１番左側に行番号を付与されます。
pandasでは便利な機能がたくさんあります。indexとして、列を指定し日付として扱う形にすると
すごく便利に使えるので覚えておいてください。
以下の例ではordered_atをindexとして扱い、曜日を付与した形で
pandasのデータフレームを新たに作るとい例を記載してみました。
weekdayとoredered_atの2つでmulti-indexとなるようにしてみます

```
>>> orders_original_df = pd.read_csv('/usr/local/src/orders.csv', index_col='ordered_at', parse_dates=True)
>>> orders_original_df
                       id  user_id                           product  price
ordered_at
2017-04-24 04:52:06   103       53         Beer - Upper Canada Lager   2905
2017-04-24 06:58:14   104      304     Muffin - Blueberry Individual   9035
...                   ...      ...                               ...    ...
2017-06-05 11:07:07   230      467           Rum - Mount Gay Eclipes   1723
2017-02-16 04:00:22    86      351                     Glaze - Clear   2877

[1000 rows x 4 columns]

>>> print(orders_original_df.index.weekday)
Int64Index([0, 0, 0, 1, 1, 1, 2, 3, 3, 4,
            ...
            2, 6, 2, 6, 5, 6, 5, 1, 0, 3],
           dtype='int64', name='ordered_at', length=1000)

>>> print(orders_original_df.index.weekday_name)
Index(['Monday', 'Monday', 'Monday', 'Tuesday', 'Tuesday', 'Tuesday',
      'Wednesday', 'Thursday', 'Thursday', 'Friday',
      ...
      'Wednesday', 'Sunday', 'Wednesday', 'Sunday', 'Saturday', 'Sunday',
      'Saturday', 'Tuesday', 'Monday', 'Thursday'],
     dtype='object', name='ordered_at', length=1000)

 >>> orders_add_weekday_df = orders_original_df.set_index([orders_original_df.index.weekday, orders_original_df.index])
 >>> orders_add_weekday_df
                                   id  user_id  \
 ordered_at ordered_at
 0          2017-04-24 04:52:06   103       53
            2017-04-24 06:58:14   104      304
            2017-04-24 23:22:45   105      176
 1          2017-04-25 01:14:14   106      357
            2017-04-25 12:02:13   107      252
            2017-04-25 12:05:14   108       95
 2          2017-04-26 07:54:31   109      416
 ...                              ...      ...
 5          2017-06-24 19:30:04   299      482
 1          2016-05-10 15:02:37    10       52
 0          2017-06-05 11:07:07   230      467
 3          2017-02-16 04:00:22    86      351

                                                         product  price
ordered_at ordered_at
0          2017-04-24 04:52:06         Beer - Upper Canada Lager   2905
           2017-04-24 06:58:14     Muffin - Blueberry Individual   9035
           2017-04-24 23:22:45            Tart Shells - Sweet, 4   5884
1          2017-04-25 01:14:14                      Juice - Lime   6367
           2017-04-25 12:02:13                 Lettuce - Iceberg   8975
           2017-04-25 12:05:14          Chicken Thigh - Bone Out   6979
2          2017-04-26 07:54:31                        Water, Tap   5745
...                                                          ...    ...
1          2016-05-10 15:02:37                    Ginger - Fresh   5614
0          2017-06-05 11:07:07           Rum - Mount Gay Eclipes   1723
3          2017-02-16 04:00:22                     Glaze - Clear   2877

[1000 rows x 4 columns]

>>> orders_add_weekday_df.index.names = ['weekday', 'date']
>>> orders_add_weekday_df.head(5)
                              id  user_id                        product  \
weekday date
0       2017-04-24 04:52:06  103       53      Beer - Upper Canada Lager
        2017-04-24 06:58:14  104      304  Muffin - Blueberry Individual
        2017-04-24 23:22:45  105      176         Tart Shells - Sweet, 4
1       2017-04-25 01:14:14  106      357                   Juice - Lime
        2017-04-25 12:02:13  107      252              Lettuce - Iceberg

                             price
weekday date
0       2017-04-24 04:52:06   2905
        2017-04-24 06:58:14   9035
        2017-04-24 23:22:45   5884
1       2017-04-25 01:14:14   6367
        2017-04-25 12:02:13   8975   

```

| オプション | 内容 |
| :-- | :-- |
| index_col | indexとするcolumn名 |
| parse_dates | datetime型で読み込むcolumn名（リストや辞書） |
| date_parser | parse_datesで指定したcolumnを読み込む自作関数 |
| na_values | 欠損値とする文字列（リスト） |
| encoding | 'Shift_JIS'など |
| sep | 区切り文字（' '：スペースの場合） |

## カラム情報やデータの確認

CSVを読み込んだ後に続けて便利なメソッドを紹介していきます

### カラム情報を見てみる

```
>>> users_original_df.columns

Index(['id', 'name', 'name_yomi', 'email', 'gender', 'age', 'birthday',
       'marriage', 'pref', 'tel', 'mobile', 'communication_carrier',
       'created_at', 'last_login_in_at', 'deleted_at'],
      dtype='object')

>>> users_original_df.describe(include = 'all')

>>> users_original_df.columns
Index(['id', 'name', 'name_yomi', 'email', 'gender', 'age', 'birthday',
       'marriage', 'pref', 'tel', 'mobile', 'communication_carrier',
       'created_at', 'last_login_in_at', 'deleted_at'],
      dtype='object')

>>> list(users_original_df.columns)
['id', 'name', 'name_yomi', 'email', 'gender', 'age', 'birthday', 'marriage', 'pref', 'tel', 'mobile', 'communication_carrier', 'created_at', 'last_login_in_at', 'deleted_at']
```

### カラム情報を見てみる

```
>>> users_original_df.describe(include = 'all')
```

| オプション | 内容 |
| :-- | :-- |
| count | そのカラムの件数 |
| mean | 平均 |
| std | 標準偏差 |
| min | 最小値 |
| 25% | 第一四分位数 |
| 50% | 第二四分位数 |
| 75% | 第三四分位数 |
| max | 最大値 |

## データの抽出

pandasもSQLと同じようにデータの抽出が行えます。

### ラベル指定した抽出

```
df.loc ラベル指定

df.loc[['row_2','row_3']] # 行ラベルを指定
df.loc[:, ['col_1','col_2']] # 列ラベルを指定
df.loc[['row_2','row_3'], ['col_1','col_2']] # 行と列ラベルを指定
df.loc[[False,False,True,True],[False,True,True]] # boolean で指定
```

実際に性別、通信キャリアの列だけを抽出するとするとこうなります。

```
>>> users_original_df.loc[:, ['gender','communication_carrier']]
```

### 列番号、行番号を指定した抽出(可読性が悪いのでアンチパターン)

```
df.iloc 行,列番号指定

df.iloc[[2,3]] # 行番号を指定
df.iloc[:, [1,2]] # 列番号を指定
df.iloc[[2,3], [1,2]] # 行、列番号を指定
df.iloc[2:4,1:3] # 行、列番号をスライスで指定
df.iloc[[False,False,True,True],[False,True,True]] # boolean で指定
```

```
>>> users_original_df.iloc[:, [1,2]]
```

### データの中身を条件にした抽出

```
>>> orders_original_df.loc[(orders_original_df['ordered_at'] >= '2016-07-03') & (orders_original_df['ordered_at'] <= '2017-04-24'), :]

>>> users_original_df.loc[(users_original_df['gender'] == '男') & (users_original_df['age'] < 50 ), :]

>>> orders_original_df.query('"2016-07-03" <= ordered_at < "2017-04-24"')
```


## 欠損値

ここからは
統計や機械学習周りで大きい影響を与える
「欠損値」の取扱を見ていきましょう。


### 未入力値の除去
特定のカラムに欠損値があった場合に削除する
オプションの「subset」は該当する列にNaNが含まれるデータを除去出来る。
オプションの「axis=0」は行を削除、「axis=1」は列を削除、

```
>>> users_original_df.describe(include='all')
                id   name name_yomi                       email gender  \
count   500.000000    500       500                         497    498
unique         NaN    500       500                         497      2
top            NaN  大竹 博之   なませ はなこ  ookawa_natsumi@example.com      女
freq           NaN      1         1                           1    255
mean    250.500000    NaN       NaN                         NaN    NaN
std     144.481833    NaN       NaN                         NaN    NaN
min       1.000000    NaN       NaN                         NaN    NaN
25%     125.750000    NaN       NaN                         NaN    NaN
50%     250.500000    NaN       NaN                         NaN    NaN
75%     375.250000    NaN       NaN                         NaN    NaN
max     500.000000    NaN       NaN                         NaN    NaN

■ 該当する列を対象に欠損値を含む行を除去

>>> users_dropna_df = users_original_df.dropna(subset=['email'])

>>> users_dropna_df.describe(include='all')
                id   name name_yomi                       email gender  \
count   497.000000    497       497                         497    497
unique         NaN    497       497                         497      2
top            NaN  大竹 博之   なませ はなこ  ookawa_natsumi@example.com      女
freq           NaN      1         1                           1    254
mean    251.408451    NaN       NaN                         NaN    NaN
std     144.373396    NaN       NaN                         NaN    NaN
min       1.000000    NaN       NaN                         NaN    NaN
25%     127.000000    NaN       NaN                         NaN    NaN
50%     252.000000    NaN       NaN                         NaN    NaN
75%     376.000000    NaN       NaN                         NaN    NaN
max     500.000000    NaN       NaN                         NaN    NaN

■ df.dropna(axis=0) 行を対象にした欠損値の除去

>>> users_original_df.dropna(axis=0)

■ df.dropna(axis=1) 列を対象にした欠損値の除去

>>> users_original_df.dropna(axis=1)
```

### 欠損値の埋め処理

```
■ 0による穴埋め
df = df.fillna(0)

>>> users_original_df['age']
0      24.0
1      81.0
2      83.0
3      78.0
4      74.0
5      15.0
6      21.0
7      73.0
8      15.0
9      84.0
10     95.0
11     15.0
12     48.0
13     20.0
14     15.0
15     47.0
16     58.0
17     13.0
18     42.0
19     50.0
20      NaN ★
21     31.0

>>> users_original_df['age'].describe()
count    498.000000　★
mean      54.891566
std       25.884442
min       13.000000
25%       31.250000
50%       55.000000
75%       79.000000
max       98.000000
Name: age, dtype: float64

>>> users_original_df['age'].fillna(0)
0      24.0
1      81.0
2      83.0
3      78.0
4      74.0
5      15.0
6      21.0
7      73.0
8      15.0
9      84.0
10     95.0
11     15.0
12     48.0
13     20.0
14     15.0
15     47.0
16     58.0
17     13.0
18     42.0
19     50.0
20      0.0　★
21     31.0

>>> users_original_df['age'].fillna(0).describe()
count    500.000000　★
mean      54.672000
std       26.064288
min        0.000000
25%       31.000000
50%       55.000000
75%       79.000000
max       98.000000
Name: age, dtype: float64


>>> users_original_df['age'].fillna(0).describe()
count    500.000000
mean      54.672000
std       26.064288
min        0.000000
25%       31.000000
50%       55.000000
75%       79.000000
max       98.000000
Name: age, dtype: float64

■ forward 穴埋め(先埋め（欠損値の直前）)
df = df.fillna(method='ffill')  # forward  = indexの増加方向 ＝ DataFrameの下方向

>>> users_original_df['age'].fillna(method='ffill')
0      24.0
1      81.0
2      83.0
3      78.0
4      74.0
5      15.0
6      21.0
7      73.0
8      15.0
9      84.0
10     95.0
11     15.0
12     48.0
13     20.0
14     15.0
15     47.0
16     58.0
17     13.0
18     42.0
19     50.0
20     50.0 ★
21     31.0

■ forward 穴埋め(後埋め（欠損値の直後）)
df = df.fillna(method='bfill')  # backward = indexの減少方向 ＝ DataFrameの上方向

>>> users_original_df['age'].fillna(method='bfill')
0      24.0
1      81.0
2      83.0
3      78.0
4      74.0
5      15.0
6      21.0
7      73.0
8      15.0
9      84.0
10     95.0
11     15.0
12     48.0
13     20.0
14     15.0
15     47.0
16     58.0
17     13.0
18     42.0
19     50.0
20     31.0　★
21     31.0

■ df.interpolate（補間）
df = df.interpolate(method='values') #値に欠損値がある場合に
※ index,linerなど色々あるので調べてみてください。

>>> users_original_df['age'].interpolate(method='values')
0      24.0
1      81.0
2      83.0
3      78.0
4      74.0
5      15.0
6      21.0
7      73.0
8      15.0
9      84.0
10     95.0
11     15.0
12     48.0
13     20.0
14     15.0
15     47.0
16     58.0
17     13.0
18     42.0
19     50.0
20     40.5
21     31.0
22     24.0


>>> users_original_df['interpolate_age'] = users_original_df['age'].interpolate(method='linear')
```

## 集計するための前処理1

```
>>> orders_groupby_user_df =  orders_original_df.groupby('user_id').size().to_frame().reset_index()
>>> orders_groupby_user_df = orders_groupby_user_df.join(orders_original_df.groupby('user_id')['price'].sum(), how='inner')
>>> orders_groupby_user_df.columns = ['id', 'order_count', 'ltv']
>>> orders_groupby_user_df.head(3)
   id  order_count    ltv
1   2            3  13910
2   3            4   8859
3   4            1  21042

>>> users_original_df.join(orders_groupby_user_df)
>>> users_with_ltv_df = pd.merge(users_original_df, orders_groupby_user_df, how='left')
>>> users_with_ltv_df = pd.merge(users_original_df, orders_groupby_user_df, how='left')
>>> users_with_ltv_df.describe()
id         age  interpolate_age  order_count           ltv
count  500.000000  498.000000       500.000000   385.000000    385.000000
mean   250.500000   54.891566        54.896000     2.272727  11341.763636
std    144.481833   25.884442        25.851243     1.309385   8184.164586
min      1.000000   13.000000        13.000000     1.000000      1.000000
25%    125.750000   31.250000        31.750000     1.000000   5426.000000
50%    250.500000   55.000000        55.000000     2.000000   9683.000000
75%    375.250000   79.000000        79.000000     3.000000  15591.000000
max    500.000000   98.000000        98.000000     7.000000  45361.000000

>>> users_with_ltv_df .head(3)
id    name name_yomi                        email gender   age   birthday  \
0   1  菅澤 菜々美  すがさわ ななみ  sugasawa_nanami@example.com      女  24.0   1994/4/3
1   2   早美 寿明  はやみ としあき  hayami_toshiaki@example.com      男  81.0   1936/5/6
2   3   小高 美咲   こだか みさき    kodaka_misaki@example.com      女  83.0  1934/9/12

marriage pref           tel         mobile communication_carrier  \
0       既婚  福岡県  076-574-8128  080-5780-6228                    au
1       既婚  京都府  030-360-3241  080-7765-4316                ソフトバンク
2       既婚  石川県  097-756-3099  080-2275- 338                   ドコモ

         created_at     last_login_in_at           deleted_at  \
0  2016/04/02 20:04:14  2017/06/23 22:57:56                  NaN
1   2016/04/03 4:58:21  2017/06/22 12:58:26  2018/04/17 23:52:26
2   2016/04/03 8:06:23   2017/06/04 6:26:15                  NaN

interpolate_age  order_count      ltv
0             24.0          NaN      NaN
1             81.0          3.0  13910.0
2             83.0          4.0   8859.0

>>> users_with_ltv_df[['order_count','ltv']] = users_with_ltv_df[['order_count','ltv']].fillna(0)
>>> users_with_ltv_df.head(3)
    id    name name_yomi                        email gender   age   birthday  \
0   1  菅澤 菜々美  すがさわ ななみ  sugasawa_nanami@example.com      女  24.0   1994/4/3
1   2   早美 寿明  はやみ としあき  hayami_toshiaki@example.com      男  81.0   1936/5/6
2   3   小高 美咲   こだか みさき    kodaka_misaki@example.com      女  83.0  1934/9/12

  marriage pref           tel         mobile communication_carrier  \
0       既婚  福岡県  076-574-8128  080-5780-6228                    au
1       既婚  京都府  030-360-3241  080-7765-4316                ソフトバンク
2       既婚  石川県  097-756-3099  080-2275- 338                   ドコモ

            created_at     last_login_in_at           deleted_at  \
0  2016/04/02 20:04:14  2017/06/23 22:57:56                  NaN
1   2016/04/03 4:58:21  2017/06/22 12:58:26  2018/04/17 23:52:26
2   2016/04/03 8:06:23   2017/06/04 6:26:15                  NaN

   interpolate_age  order_count      ltv
0             24.0          0.0      0.0
1             81.0          3.0  13910.0
2             83.0          4.0   8859.0

>>> users_with_ltv_df.to_csv('/usr/local/src/users_with_ltv.csv', index=False)
```

## 集計するための前処理2

```

>>> users_with_ltv_df.groupby('gender').size()
gender
女    255
男    243
dtype: int64

>>> users_with_ltv_df[['gender','interpolate_age']].groupby('gender').agg(['min', 'max'])
       interpolate_age
                   min   max
gender
女                 13.0  98.0
男                 13.0  98.0

>>> users_gender_age_df = users_with_ltv_df[['gender','interpolate_age','communication_carrier','marriage','pref','order_count','ltv']]

>>> print(pd.crosstab(users_gender_age_df.gender, users_gender_age_df.order_count))

>>> print(pd.crosstab(users_gender_age_df.pref, users_gender_age_df.gender))
gender   女   男
pref
三重県      6   4
京都府      8   4
佐賀県      3   1
兵庫県     12  18
北海道     15   9
千葉県     15  10
和歌山県     0   1

>>> def age_class(age):
  if age < 10:
    return '0-9'
  elif age < 20:
    return '10-19'
  elif age < 30:
    return '20-29'
  elif age < 40:
    return '30-39'
  elif age < 50:
    return '40-49'
  elif age < 60:
    return '50-59'
  elif age < 70:
    return '60-69'
  elif age < 80:
    return '70-79'
  elif age < 90:
    return '80-89'
  elif age < 100:
    return '90-99'
  else:
    return '100-'

>>> users_gender_age_df['byage'] = users_gender_age_df['interpolate_age'].apply(age_class)
>>> print(pd.crosstab([users_gender_age_df['pref']], [users_gender_age_df['gender'], users_gender_age_df['byage']]))

```
