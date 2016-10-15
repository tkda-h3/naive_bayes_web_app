# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
# from . import forms


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def hello_forms(request):
    d = {
        'input_url': request.GET.get('input_url')
    }
    return render(request, 'forms.html', d)


