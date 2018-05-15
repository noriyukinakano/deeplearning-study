
# 前処理　第3章〜コホート分析〜

## 準備
第2章で使用したデータのと顧客が購入した注文を想定したorders.csvを利用します。
編集後記

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
いつもの通り用意してあるDockerイメージを用いて、対話式pythonで学習しましょう。
Dockerイメージのコンテナにはディスプレイを接続していないため
おまじないとして固定の環境変数を設定し、対話モードでpythonを起動させます。

```bash
env DISPLAY=:0 PYTHONIOENCODING=utf-8 MPLBACKEND="agg" python3.6
```

### pandasのライブラリインポートとフォントの設定

```python3
import os.path
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
font_prop = FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
```

### CSVデータの読み込み

対話式のpythonに入ると「>>> 」と表示されます。
以下の「>>> 」の横に書いてあるのが実行するコマンドです。
まずはpandasでcsvをインポートしましょう

```python3
>>> orders_original_df = pd.read_csv('/usr/local/src/orders.csv')
>>> orders_original_df

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

### データ型の変更
ordered_atが文字列として認識されていることがあるため
一度、datetime型に変更を行います。

```
>>> orders_original_df['ordered_at'] = pd.to_datetime(orders_original_df['ordered_at'])
```

### 購入月を取得
今回のコホート分析は、初回購入月からN月経過したらという分析を想定しているため
ordered_atを元に、%Y-%mの形式に変更した「order_period」を取得しています

```
>>> orders_original_df['order_period'] = orders_original_df.ordered_at.apply(lambda x: x.strftime('%Y-%m'))
```

### 購入者をindexにしたGroupDataFrameを作成
顧客IDをインデックスに指定し、顧客ID毎に初回購入月を付与しています。
cohort_group毎にグループ化され、経過月数毎の推移が見れるようになります。

```
>>> cohort_df = orders_original_df.set_index('user_id')
>>> cohort_df.head(2)

id                        product  price          ordered_at  \
user_id
53       103      Beer - Upper Canada Lager   2905 2017-04-24 04:52:06
304      104  Muffin - Blueberry Individual   9035 2017-04-24 06:58:14

order_period
user_id
53           2017-04
304          2017-04

>>> cohort_df['cohort_group'] = cohort_df.groupby(level=0)['ordered_at'].min().apply(lambda x: x.strftime('%Y-%m'))
>>> cohort_df = cohort_df.reset_index()
>>> cohort_df = cohort_df.sort_values('user_id')

>>> cohort_df.head(4)
     user_id   id                      product  price          ordered_at  \
742        1  856   Rum - Dark, Bacardi, Black   5690 2018-01-22 15:00:24
872        1  945  Rum - Light, Captain Morgan   8220 2018-03-07 09:21:30
412        2  553          Beef - Inside Round   4764 2017-09-26 00:27:44
132        2  249   Noodles - Cellophane, Thin   1720 2017-06-10 23:00:02

    order_period cohort_group
742      2018-01      2018-01
872      2018-03      2018-01
412      2017-09      2017-06
132      2017-06      2017-06
```

次に集計を行うために初回購入月(cohort_group)と購入月(order_period)を軸にしたGroupDataFrameを生成します。
それからaggメソッドを利用し
・顧客ID(user_id)のユニーク数
・注文ID(id)のユニーク数
・購入金額の総額
を算出しています。

```
>>> grouped = cohort_df.groupby(['cohort_group', 'order_period'])

>>> cohorts = grouped.agg({'user_id': pd.Series.nunique,
                       'id': pd.Series.nunique,
                       'price': np.sum})

>>> cohorts.head(3)
                          user_id  id  price
cohort_group order_period
2016-04      2016-04             5   6  11850
            2017-03             1   1   2329
            2017-04             1   1    380

>>> cohorts.rename(columns={'user_id': 'total_users',
    'id': 'total_orders'}, inplace=True)

>>> cohorts.head(3)
                           total_users  total_orders  price
cohort_group order_period
2016-04      2016-04                 5             6  11850
             2017-03                 1             1   2329
             2017-04                 1             1    380
```

### 経過月数の付与をデータの整合性の確認
実際に開発する際には、確認で行う想定したデータがあっているかどうかの確認も
せっかくなので紹介します。

```
>>> def cohort_period(df):
...   df['cohort_period'] = np.arange(len(df)) + 1
...   return df
...
>>> cohorts = cohorts.groupby(level=0).apply(cohort_period)
>>> cohorts.head(3)
                           total_users  total_orders  price  cohort_period
cohort_group order_period
2016-04      2016-04                 5             6  11850              1
             2017-03                 1             1   2329              2
             2017-04                 1             1    380              3
```

今までに学習したpandasでの抽出を使っているので
分かると思いますが、分からない人はさかのぼって復習してみてください

```
>>> x = cohort_df[(cohort_df.cohort_group == '2016-04') & (cohort_df.order_period == '2016-04')]
>>> x
    index  user_id  id                      product  price  \
32    927       18   1                     Sultanas    841
42    944       25   3    Melon - Watermelon Yellow    703
45    793       25   2          Beer - Steamwhistle   1189
48    650       26   4  Shichimi Togarashi Peppeers   1299
51    847       27   5                       Kiwano   7373
56    750       29   6            Plasticspoonblack    445

            ordered_at order_period cohort_group
32 2016-04-12 17:58:35      2016-04      2016-04
42 2016-04-17 01:08:52      2016-04      2016-04
45 2016-04-17 01:08:52      2016-04      2016-04
48 2016-04-17 18:01:08      2016-04      2016-04
51 2016-04-17 23:30:25      2016-04      2016-04
56 2016-04-22 06:52:39      2016-04      2016-04

>>> y = cohorts.ix[('2016-04', '2016-04')]

>>> y
total_users          5
total_orders         6
price            11850
cohort_period        1
Name: (2016-04, 2016-04), dtype: int64
```
抽出している内容は上記の通りです。
初回購入月(cohort_group)が「2016-04」かつ購入月(order_period)が「2016-04」の
データを抽出しています。

pandasに用意されている「assert」を利用し
xのデータに含まれるユニークなユーザー数と
yで取得しているユーザー数が一致している/一致していないを検証してみましょう。

```
>>> assert(x['user_id'].nunique() != y['total_users'])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError

>>> assert(x['user_id'].nunique() == y['total_users'])

>>> assert(x['price'].sum().round(2) == y['price'].round(2))
>>> assert(x['id'].nunique() == y['total_orders'])
```

いかがでしょうか？
検証内容に合致していない場合は「AssertionError」が出力している事が分かります。
初月以外のデータも確認してみましょう。

```
>>> x = cohort_df[(cohort_df.cohort_group == '2016-04') & (cohort_df.order_period == '2017-10')]
>>> y = cohorts.ix[('2016-04', '2017-10')]
>>>
>>> assert(x['user_id'].nunique() == y['total_users'])
>>> assert(x['price'].sum().round(2) == y['price'].round(2))
>>> assert(x['id'].nunique() == y['total_orders'])
```

### コホート分析のデータを整形する
購入月毎に異なると同じ軸で集計が出来ないために
初回購入月(cohort_group)と経過月数(cohort_period)をインデックスに指定し直します


```
>>> cohorts.head(10)
                           total_users  total_orders  price  cohort_period
cohort_group order_period
2016-04      2016-04                 5             6  11850              1
             2017-03                 1             1   2329              2
             2017-04                 1             1    380              3
             2017-05                 1             1   5437              4
             2017-06                 2             2  17114              5
             2017-07                 1             1   6993              6
             2017-10                 4             5  18320              7
2016-05      2016-05                 5             7  46339              1
             2017-04                 1             1   2905              2
             2017-05                 1             1   7674              3

>>> cohorts.reset_index(inplace=True)
>>> cohorts.head(10)
 cohort_group order_period  total_users  total_orders  price  cohort_period
0      2016-04      2016-04            5             6  11850              1
1      2016-04      2017-03            1             1   2329              2
2      2016-04      2017-04            1             1    380              3
3      2016-04      2017-05            1             1   5437              4
4      2016-04      2017-06            2             2  17114              5
5      2016-04      2017-07            1             1   6993              6
6      2016-04      2017-10            4             5  18320              7
7      2016-05      2016-05            5             7  46339              1
8      2016-05      2017-04            1             1   2905              2
9      2016-05      2017-05            1             1   7674              3

>>> cohorts.head(10)
                           order_period  total_users  total_orders  price
cohort_group cohort_period
2016-04      1                  2016-04            5             6  11850
             2                  2017-03            1             1   2329
             3                  2017-04            1             1    380
             4                  2017-05            1             1   5437
             5                  2017-06            2             2  17114
             6                  2017-07            1             1   6993
             7                  2017-10            4             5  18320
2016-05      1                  2016-05            5             7  46339
             2                  2017-04            1             1   2905
             3                  2017-05            1             1   7674
```

次にマルチインデックスのはられている1階層目(cohort_group)で集計を行い
初回購入月(cohort_group)毎の初月のcohort_periodを取得します。

```
>>> cohort_group_size = cohorts['total_users'].groupby(level=0).first()
>>> cohort_group_size.head(3)
cohort_group
2016-04    5
2016-05    5
2016-06    7
```

この状態ではデータが見えづらいので
縦横変換を「unstack」を用いて行います

```
>>> cohorts['total_users'].head(10)
cohort_group  cohort_period
2016-04       1                5
              2                1
              3                1
              4                1
              5                2
              6                1
              7                4
2016-05       1                5
              2                1
              3                1

>>> cohorts['total_users'].unstack(0).head(10)
cohort_group   2016-04  2016-05  2016-06  2016-07  2016-08  2016-09  2016-10  \
cohort_period
1                  5.0      5.0      7.0      8.0      7.0      6.0      6.0
2                  1.0      1.0      1.0      2.0      2.0      1.0      3.0
3                  1.0      1.0      2.0      1.0      1.0      1.0      1.0
4                  1.0      1.0      4.0      1.0      1.0      1.0      1.0
5                  2.0      1.0      2.0      NaN      1.0      1.0      1.0
6                  1.0      1.0      2.0      NaN      1.0      1.0      2.0
7                  4.0      1.0      2.0      NaN      2.0      NaN      2.0
8                  NaN      1.0      NaN      NaN      1.0      NaN      1.0
9                  NaN      1.0      NaN      NaN      1.0      NaN      NaN
10                 NaN      1.0      NaN      NaN      1.0      NaN      NaN
```

次に「divide」を使ってcohort_group毎の全体母数からの割合をそれぞれ取得します。

```
>>> user_retention = cohorts['total_users'].unstack(0).divide(cohort_group_size, axis=1)
>>> user_retention.head(3)
cohort_group   2016-04  2016-05   2016-06  2016-07   2016-08   2016-09  \
cohort_period
1                  1.0      1.0  1.000000    1.000  1.000000  1.000000
2                  0.2      0.2  0.142857    0.250  0.285714  0.166667
3                  0.2      0.2  0.285714    0.125  0.142857  0.166667

cohort_group    2016-10  2016-11   2016-12  2017-01   ...      2017-07  \
cohort_period                                         ...
1              1.000000    1.000  1.000000      1.0   ...     1.000000
2              0.500000    0.125  0.166667      0.4   ...     0.098039
3              0.166667    0.250  0.166667      0.2   ...     0.156863

cohort_group   2017-08  2017-09   2017-10   2017-11   2017-12   2018-01  \
cohort_period
1              1.00000     1.00  1.000000  1.000000  1.000000  1.000000
2              0.15625     0.20  0.166667  0.227273  0.095238  0.166667
3              0.09375     0.08  0.083333  0.181818  0.095238  0.111111

cohort_group    2018-02  2018-03  2018-04
cohort_period
1              1.000000      1.0      1.0
2              0.166667      NaN      NaN
3                   NaN      NaN      NaN

[3 rows x 25 columns]
```

### 可視化
テストデータがあまり綺麗でないのでイメージがわかないかもしれませんが
可視化として
・特定3ヶ月の残存率の推移を見るグラフ
・全期間の残存率が分かるヒートマップグラフ
を出力して終了したいと思います。

```
user_retention[['2017-07', '2017-08', '2017-09']].plot(figsize=(10,5))
plt.title('Cohorts: User Retention')
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 12)
plt.ylabel('% of Cohort Purchasing')
plt.savefig('/usr/local/src/cohort3month_line.png')
plt.clf()
```

```
sns.set(style='white')
plt.figure(figsize=(12, 8))
plt.title('Cohorts: User Retention')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%');
plt.savefig('/usr/local/src/cohort_heatmap.png')
plt.clf()
```

無事に出来ましたか?

## 編集後記
今回は集計を使ったコホート分析を学習しました。どうだったでしょうか？
ディープラーニングに入る前の前提知識の理解が深まってきたのではないでしょうか？
次回からは少しずつディープラーニングの世界に入っていくのでお楽しみに。

### 前回の宿題の答え

第2章〜前処理〜で利用した内容を元に

「age」の欠損値を「liner」で補間した後、
「order_count」、「byage」、「ltv」を求め
元のusers.csvと結合を行い、購入履歴のない顧客はNaNでなくゼロ埋めし
「gender」、「pref」、「marriage」を利用し
各項目(2個）のクロス集計を求めよ。
また余力がある人は、各項目をpairplotし
相関を確認せよ

#### クロス集計

```
import os.path
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
font_prop = FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

users_original_df = pd.read_csv('/usr/local/src/users.csv')
orders_original_df = pd.read_csv('/usr/local/src/orders.csv')
users_original_df['interpolate_age'] = users_original_df['age'].interpolate(method='linear')
orders_groupby_user_df = orders_original_df.groupby('user_id')['id'].count().to_frame().reset_index()
orders_groupby_user_sum_df = orders_original_df.groupby('user_id')['price'].sum().to_frame().reset_index()
orders_groupby_user_df = pd.merge(orders_groupby_user_df, orders_groupby_user_sum_df, how="left", on="user_id")
orders_groupby_user_df.columns = ['id', 'order_count', 'ltv']
users_with_ltv_df =  pd.merge(users_original_df, orders_groupby_user_df, how='left', on="id")
users_gender_age_df = users_with_ltv_df[['gender','age','communication_carrier','marriage','pref','order_count','ltv']]
users_gender_age_df[['ltv']] = users_gender_age_df[['ltv']].fillna(0)
users_gender_age_df[['order_count']] = users_gender_age_df[['order_count']].fillna(0)

def age_class(age):
  if age < 10:
    return '0'
  elif age < 20:
    return '10'
  elif age < 30:
    return '20'
  elif age < 40:
    return '30'
  elif age < 50:
    return '40'
  elif age < 60:
    return '50'
  elif age < 70:
    return '60'
  elif age < 80:
    return '70'
  elif age < 90:
    return '80'
  elif age < 100:
    return '90'
  else:
    return '100'

users_gender_age_df['byage'] = users_gender_age_df['age'].apply(age_class).to_frame()
users_gender_age_df.byage = users_gender_age_df.byage.astype('float64')
users_gender_age_df[['byage','order_count']].groupby('byage').mean()
users_gender_age_df[['byage','ltv']].groupby('byage').mean()

analysys_df = pd.merge(users_gender_age_df[['byage','order_count']].groupby('byage').mean().reset_index(),users_gender_age_df[['byage','ltv']].groupby('byage').mean().reset_index(), how="left", on="byage")

ct = pd.crosstab(users_gender_age_df.byage, users_gender_age_df.communication_carrier)

stacked = ct.stack().reset_index().rename(columns={0:'value'})

sns.barplot(x=stacked.byage, y = stacked.value ,hue=stacked.communication_carrier)
plt.savefig('/usr/local/src/barplot.png')
plt.clf()

ct2 = pd.crosstab(users_gender_age_df.gender, users_gender_age_df.marriage)
stacked2 = ct2.stack().reset_index().rename(columns={0:'value'})
sns.barplot(x=stacked2.gender, y=stacked2.value ,hue=stacked2.marriage)
plt.savefig('/usr/local/src/barplot2.png')
plt.clf()

ct3 = pd.crosstab(users_gender_age_df.gender, users_gender_age_df.pref)
stacked3 = ct3.stack().reset_index().rename(columns={0:'value'})
sns.barplot(x=stacked3.gender, y=stacked3.value ,hue=stacked3.pref)
plt.savefig('/usr/local/src/barplot3.png')
plt.clf()
```

#### pairplotで相関を調べる

```
# coding:utf-8
from __future__ import print_function, division

import os.path
import sys
import pandas as pd
import seaborn
import numpy as np
import matplotlib as mpl
mpl.use('Agg')

orders_original_df = pd.read_csv('/usr/local/src/orders.csv')
users_original_df = pd.read_csv('/usr/local/src/users.csv')
users_original_df['deleted_at'] = pd.to_datetime(users_original_df['deleted_at'])
users_original_df['interpolate_age'] = users_original_df['age'].interpolate(method='linear')
orders_groupby_user_df = orders_original_df.groupby('user_id')['id'].count().to_frame().reset_index()
orders_groupby_user_sum_df = orders_original_df.groupby('user_id')['price'].sum().to_frame().reset_index()
orders_groupby_user_df = pd.merge(orders_groupby_user_df, orders_groupby_user_sum_df, how="left", on="user_id")
orders_groupby_user_df.columns = ['id', 'order_count', 'ltv']

def deleted_class(deleted_at):
  if pd.isnull(deleted_at):
    return 0
  else:
    return 1

def gender_class(gender):
    if  gender == '未入力':
        return 0
    elif gender == '男':
        return 1
    elif gender == '女':
        return 2
    elif pd.isnull(gender):
        return 1
    else:
        return 99

def age_class(age):
  if age < 10:
    return 0
  elif age < 20:
    return 10
  elif age < 30:
    return 20
  elif age < 40:
    return 30
  elif age < 50:
    return 40
  elif age < 60:
    return 50
  elif age < 70:
    return 60
  elif age < 80:
    return 70
  elif age < 90:
    return 80
  elif age < 100:
    return 90
  elif pd.isnull(age):
      return np.nan
  else:
    return 100

def pref_class(pref):
  if pref == '北海道':
    return 1
  elif pref == '青森県':
    return 2
  elif pref == '岩手県':
    return 3
  elif pref == '宮城県':
    return 4
  elif pref == '秋田県':
    return 5
  elif pref == '山形県':
    return 6
  elif pref == '福島県':
    return 7
  elif pref == '茨城県':
    return 8
  elif pref == '栃木県':
    return 9
  elif pref == '群馬県':
    return 10
  elif pref == '埼玉県':
    return 11
  elif pref == '千葉県':
    return 12
  elif pref == '東京都':
    return 13
  elif pref == '神奈川県':
    return 14
  elif pref == '新潟県':
    return 15
  elif pref == '富山県':
    return 16
  elif pref == '石川県':
    return 17
  elif pref == '福井県':
    return 18
  elif pref == '山梨県':
    return 19
  elif pref == '長野県':
    return 20
  elif pref == '岐阜県':
    return 21
  elif pref == '静岡県':
    return 22
  elif pref == '愛知県':
    return 23
  elif pref == '三重県':
    return 24
  elif pref == '滋賀県':
    return 25
  elif pref == '京都府':
    return 26
  elif pref == '大阪府':
    return 27
  elif pref == '兵庫県':
    return 28
  elif pref == '奈良県':
    return 29
  elif pref == '和歌山県':
    return 30
  elif pref == '鳥取県':
    return 31
  elif pref == '島根県':
    return 32
  elif pref == '岡山県':
    return 33
  elif pref == '広島県':
    return 34
  elif pref == '山口県':
    return 35
  elif pref == '徳島県':
    return 36
  elif pref == '香川県':
    return 37
  elif pref == '愛媛県':
    return 38
  elif pref == '高知県':
    return 39
  elif pref == '福岡県':
    return 40
  elif pref == '佐賀県':
    return 41
  elif pref == '長崎県':
    return 42
  elif pref == '熊本県':
    return 43
  elif pref == '大分県':
    return 44
  elif pref == '宮崎県':
    return 45
  elif pref == '鹿児島県':
    return 46
  elif pref == '沖縄県':
    return 47
  elif pd.isnull(pref):
      return np.nan
  else:
    return 99

def marriage_class(marriage):
    if  marriage == '未婚':
        return 0
    elif marriage == '既婚':
        return 1
    elif pd.isnull(marriage):
        return np.nan
    else:
        return 99

def communication_carrier_class(communication_carrier):
    if  communication_carrier == 'ドコモ':
        return 1
    elif communication_carrier == 'ソフトバンク':
        return 2
    elif communication_carrier == 'au':
        return 3
    elif communication_carrier == 'ツーカー':
        return 4
    elif pd.isnull(communication_carrier):
        return np.nan
    else:
        return 99

users_original_df['deleted'] = users_original_df['deleted_at'].apply(deleted_class).to_frame()
users_original_df['byage'] = users_original_df['interpolate_age'].apply(age_class).to_frame()
users_original_df['gender_id'] = users_original_df['gender'].apply(gender_class).to_frame()
users_original_df['pref_id'] = users_original_df['pref'].apply(pref_class).to_frame()
users_original_df['marriage_id'] = users_original_df['marriage'].apply(marriage_class).to_frame()
users_original_df['communication_carrier_id'] = users_original_df['communication_carrier'].apply(communication_carrier_class).to_frame()

users_with_ltv_df =  pd.merge(users_original_df, orders_groupby_user_df, how='left', on="id")
users_with_ltv_df[['ltv']] = users_with_ltv_df[['ltv']].fillna(0)
users_with_ltv_df[['order_count']] = users_with_ltv_df[['order_count']].fillna(0)

target_columns = ['byage', 'gender_id', 'pref_id', 'marriage_id', 'communication_carrier_id', 'order_count', 'ltv']
target_label = 'deleted'

y = users_with_ltv_df[target_label]
len(y)

X = users_with_ltv_df[target_columns]
len(X)

W = pd.merge(X, pd.DataFrame(y), right_index=True, left_index=True)
seaborn.pairplot(W, hue = target_label)
plt.savefig('/data/pairplot_noscalled.png')
plt.clf()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
Z = pd.merge(pd.DataFrame(X_scaled), pd.DataFrame(y), right_index=True, left_index=True)

target_columns.append(target_label)
Z.columns = target_columns
plt.figure(figsize=(50, 50))
seaborn.pairplot(Z, hue = target_label)
plt.savefig('/data/pairplot_scalled.png')
plt.clf()
```

### 次回までの宿題
users.csvを用いて会員退会についてのコホート分析を行ってみてください。
