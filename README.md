# ナイーブベイズによる文書分類Djangoアプリ
## 実行環境
- Python (3.5.2)
- Django (1.10.2)
- beautifulsoup4 (4.5.1)
- gensim (0.13.2)
- mecab-python3 (0.7)
- numpy (1.11.2)
- scikit-learn (0.18)

## 学習結果
[learning.ipynb](https://github.com/tkda-h3/naive_bayes_web_app/blob/master/learning.ipynb)で学習し、学習結果を`pickle`で保存した。

## 使い方
### コマンドラインで学習を実行
すでに保存してある学習結果を使わずに、コマンドラインでDjangoアプリ内で学習を実行することが可能である。学習結果はリポジトリのルートディレクトリに上書き保存される。
`mysite`ディレクトリで
```
usage: python manage.py learning [-h] [--version] [-v {0,1,2,3}]
                          [--settings SETTINGS] [--pythonpath PYTHONPATH]
                          [--traceback] [--no-color] [-n N] [--save]

学習してpickleで保存します

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  -n N                  the number of scraping pages of each category (default: 1)
  --save, -s            save result of learning if this flag is set (default: False)
```

### Djangoアプリの起動
`mysite`ディレクトリで
```
$ python manage.py runserver
```
を実行

### Gunosyの記事URLのカテゴリ予測
1. `http://127.0.0.1:8000/`にアクセス
2. Gunosyの記事URLをフォームに入力して送信
3. 入力されたURLの記事の予測カテゴリを表示
