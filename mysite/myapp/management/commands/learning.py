# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from itertools import starmap
from gensim import corpora, matutils
import numpy as np
from sklearn.cross_validation import StratifiedKFold
import pickle

from ._core import *
from django.conf import settings
import os

class Command(BaseCommand):
    help = '学習してpickleで保存します'

    def add_arguments(self, parser):
        parser.add_argument('-n', default=1, type=int, help='the number of scraping pages of each category')
        parser.add_argument('--save','-s', action='store_true', default=False, help='save result of learning if this flag is set (default: False)')
        
    def handle(self, *args, **options):
        print(settings.BASE_DIR, 'BASE_DIR')
        print(os.path.join(settings.BASE_DIR, '../'))

        PAGE_NUM = options['n']
        SAVE_FLAG = options['save']
        # self.stdout.write(str(page_num), ending='\n')

        categories = get_categories("https://gunosy.com/")
        all_contents = []
        all_links = []
        all_labels = []
        for i,url_info in enumerate(categories[:3]):
            for page_num in range(1,PAGE_NUM+1):
                pager_query = '?page=%d' % page_num
                url = url_info[0] + pager_query
                print(url)
                links,contents = get_links_and_contents(url)
                all_links.extend(links)
                all_contents.extend(contents)
                all_labels.extend([i] * len(links))    

        res = get_words_matrix(all_contents)
        dictionary = corpora.Dictionary(res)
        dictionary.filter_extremes(no_below=10 , no_above=0.2)
        # [ [(w_id1, w_id1_cnt), (w_id2, w_id2_cnt),...] ,
        #   [(w_id1, w_id1_cnt), (w_id2, w_id2_cnt),...] ,
        # ]
        bows = [dictionary.doc2bow(x) for x in res]

        X = np.array([(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0]) 
                           for vec in bows])
        y = np.array(all_labels)

        # cross validation
        skf = StratifiedKFold(y, n_folds=5, shuffle=True, random_state = 7654)
        scores = []
        for train_index, test_index in skf:
            #print(train_index, test_index)
            train_X, test_X = X[train_index], X[test_index]
            train_y, test_y = y[train_index], y[test_index]  
            score = evaluate_model(train_X,test_X,train_y,test_y)
            scores.append(score)
        scores = np.array(scores)
        print(scores)
        print('結果' ,np.mean(scores))

        #pickleに保存
        cat_prob = calc_cat(y)
        word_cat_prob = calc_each_word_bar_cat(X,y)
        dictionary
        cvt_y_to_category_name = dict(list(starmap(lambda i,x: (i,str(x[1])), enumerate(categories))))#ラベルy から　カテゴリ名に変換するdict
        print(cvt_y_to_category_name)
        
        if SAVE_FLAG:
            def save_as_pickle(file_path, obj):
                with open(file_path, 'wb') as f:
                    pickle.dump(obj, f)

            dir_path = (os.path.join(settings.BASE_DIR, '../'))
            save_as_pickle(dir_path + 'dictionay.dump', dictionary)
            save_as_pickle(dir_path + 'cat_prob.dump', cat_prob)
            save_as_pickle(dir_path + 'word_cat_prob.dump', word_cat_prob)
            save_as_pickle(dir_path + 'cvt_y_to_category_name.dump', cvt_y_to_category_name)
            print('------ Save completed. ------')
        else:
            print('------ not saved. -------')

        
