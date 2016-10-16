# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

import sys
from naive_bayes import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def hello_forms(request): 
    d = {
        'input_url': request.GET.get('input_url'),
    }
    if d['input_url']:
        try:
            d['pred_category_name'] = get_category_name(request.GET.get('input_url'))
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


