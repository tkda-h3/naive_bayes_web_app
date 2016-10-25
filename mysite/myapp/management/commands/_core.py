# -*- coding: utf-8 -*-
#!/usr/bin/env python

from urllib.request import urlopen
from bs4 import BeautifulSoup
import MeCab
import numpy as np
from sklearn.metrics import f1_score

from ._category import Category


def get_categories(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    a_list = soup.select("body > nav > ul > li > a")[1:-1]
    #categories = list(map(lambda a: (a.get("href"), a.string), a_list))
    categories = list(map(lambda a: Category(str(a.string), a.get("href")), a_list))
    return categories


def get_content(page_url):
    html = urlopen(page_url)
    soup = BeautifulSoup(html, 'html.parser')
    content_tag = soup.select(
        "body div.main.article_main > div.article.gtm-click")
    # .encode('utf-8')
    return ('').join([text_tag.get_text() for text_tag in content_tag])


def get_links_and_contents(category_url):
    html = urlopen(category_url)
    soup = BeautifulSoup(html, 'html.parser')
    a_list = soup.select(
        "body > div > div > div.main > div.article_list.gtm-click > div.list_content > div.list_text > div.list_title > a")
    links = list(map(lambda a: a.get("href"), a_list))
    contents = list(map(lambda url: get_content(url), links))
    return links, contents


def get_words_list(text):
    mecab = MeCab.Tagger('mecabrc')
    mecab.parse('')  # これ重要！！！！ 謎のバグに対処する
    node = mecab.parseToNode(text)
    words_list = []
    while node:
        if node.feature.split(",")[0] == '名詞':
            words_list.append(node.surface.lower())
        node = node.next
    return words_list


def get_words_matrix(texts_list):
    """
    texts_list : ['text1', 'text2',... ]
    """
    return [get_words_list(text) for text in texts_list]


def calc_cat(y):
    """
    calculate P(cat)
    """
    label_kinds_num = len(np.unique(y))
    ans = np.empty(label_kinds_num)
    for i in range(label_kinds_num):
        ans[i] = len(np.argwhere(y == i)[:, 0]) / 1.0 * len(y)
    return ans


def calc_each_word_bar_cat(X, y):
    """
    calculate P(word_id1 | cat)
    """
    label_kinds_num = len(np.unique(y))
    ans = np.empty((label_kinds_num, X.shape[1]))
    for i in range(label_kinds_num):
        index = np.argwhere(y == i)[:, 0]  # index
        ans[i] = (X[index, :].sum(axis=0) + 1).astype(np.float32) / \
            (X[index, :].sum() + X.shape[1])  # laplace smoothing
    return ans


def calc_log_prob(word_cat_prob, cat_prob, doc):  # doc : 1 feature vector
    doc_word_index = np.where(doc != 0)
    each_word_prob_in_doc = word_cat_prob[
        :, doc_word_index[1]]  # docに含まれる単語の各P(word | cat)
    each_log_word_cat_prob = np.log(each_word_prob_in_doc).sum(axis=1)
    ans = np.log(cat_prob) + each_log_word_cat_prob
    return ans


def evaluate_model(train_X, test_X, train_y, test_y):
    cat_prob = calc_cat(train_y)
    word_cat_prob = calc_each_word_bar_cat(train_X, train_y)
    pred_y = []
    for vec in test_X:
        log_prob = calc_log_prob(word_cat_prob, cat_prob, (vec)[np.newaxis, :])
        pred_y.append(np.argmax(log_prob))
    pred_y = np.array(pred_y)

    score = f1_score(test_y, pred_y, average='macro')
    return score
