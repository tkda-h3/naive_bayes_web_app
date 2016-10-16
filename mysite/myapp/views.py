# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import sys
from .naive_bayes import *
import urllib

def index(request): 
    d = {
        'input_url': request.GET.get('input_url'),
    }
    if d['input_url']:
        try:
            d['pred_category_name'] = get_category_name(request.GET.get('input_url'))
        except ValueError as instance:
            print(instance, file=sys.stderr)
            d['pred_category_name'] = False
        except urllib.error.HTTPError as instance:
            print(instance, file=sys.stderr)
            d['pred_category_name'] = False
        except urllib.error.URLError as instance:
            print(instance, file=sys.stderr)
            d['pred_category_name'] = False
    
    return render(request, 'forms.html', d)


