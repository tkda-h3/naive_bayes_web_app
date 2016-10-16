# ナイーブベイズによる文書分類Djangoアプリ
## 学習
[learning.ipynb](https://github.com/tkda-h3/naive_bayes_web_app/blob/master/learning.ipynb)で学習した。

## 使い方
### Djangoアプリの起動
`site`ディレクトリで
```
$ python manage.py runserver
```
を実行

### Gunosyの記事URLのカテゴリ予測
1. `http://127.0.0.1:8000/`にアクセス
2. Gunosyの記事URLをフォームに入力して送信
3. 入力されたURLの記事の予測カテゴリを表示
