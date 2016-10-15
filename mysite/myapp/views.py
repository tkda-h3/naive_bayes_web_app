# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from prettyprint import pp
import pickle
import urllib2
from bs4 import BeautifulSoup
import MeCab
from gensim import corpora, matutils
import numpy as np
import os.path
import sys

def get_obj_from_pickle(file_path):
    with open(file_path, 'r') as f:
        return pickle.load(f)

def get_content(page_url):
    html = urllib2.urlopen(page_url)
    soup = BeautifulSoup(html, "lxml")
    content_tag = soup.select("body div.main.article_main > div.article.gtm-click")
    return ('').join( [text_tag.get_text() for text_tag in content_tag] ).encode('utf-8')

def get_words_list(text):
    mecab = MeCab.Tagger('mecabrc')
    node = mecab.parseToNode(text)
    words_list = []
    while node:
        if node.feature.split(",")[0] == '名詞':
            words_list.append(node.surface.lower())
        node = node.next
    return words_list

def calc_log_prob(word_cat_prob, cat_prob, doc): # doc : 1 feature vector
        doc_word_index = np.where(doc != 0)
        each_word_prob_in_doc  = word_cat_prob[:, doc_word_index[1]] #docに含まれる単語の各P(word | cat)
        each_log_word_cat_prob = np.log(each_word_prob_in_doc).sum(axis=1)
        ans = np.log(cat_prob) + each_log_word_cat_prob
        return ans


def predict_y_of_input_url(input_url, dictionary,word_cat_prob, cat_prob):
    text_of_input_url = get_content(input_url)    
    word_list_of_input_url = get_words_list(text_of_input_url)
    bow_of_input_url = dictionary.doc2bow(word_list_of_input_url) #[(w_id1, w_id1_cnt), (w_id2, w_id2_cnt),...] 
    test_X = np.array([matutils.corpus2dense([bow_of_input_url], num_terms=len(dictionary)).T[0]])
    log_prob = calc_log_prob(word_cat_prob,cat_prob, test_X)
    return np.argmax(log_prob)

def get_category_name(url):
    # deserialize
    dir_path = os.path.abspath('./../')+'/'
    cat_prob = get_obj_from_pickle(dir_path+'cat_prob.dump')
    word_cat_prob = get_obj_from_pickle(dir_path+'word_cat_prob.dump')
    dictionary = get_obj_from_pickle(dir_path+'dictionay.dump')
    cvt_y_to_category_name = get_obj_from_pickle(dir_path+'cvt_y_to_category_name.dump')
    pred_y_of_input_url = predict_y_of_input_url(url, dictionary, word_cat_prob, cat_prob)    
    pred_category_name_of_input_url = cvt_y_to_category_name[pred_y_of_input_url] #数字ラベルを変換
    return pred_category_name_of_input_url

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def hello_forms(request): 
    d = {
        'input_url': request.GET.get('input_url'),
    }
    if d['input_url']:
        try:
            d['pred_category_name'] = get_category_name(request.GET.get('input_url'))
            print '*'*30
            print '*****      ' + d['pred_category_name']
            print '*'*30            
        except ValueError, instance:
            print >> sys.stderr, instance
            d['pred_category_name'] = False
        except urllib2.HTTPError, instance:
            print >> sys.stderr, instance
            d['pred_category_name'] = False
        except urllib2.URLError, instance:
            print >> sys.stderr, instance
            d['pred_category_name'] = False
    
    return render(request, 'forms.html', d)


