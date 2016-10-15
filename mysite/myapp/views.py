# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
# from . import forms


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def hello_forms(request):
    d = {
        'your_name': request.GET.get('your_name')
    }
    return render(request, 'forms.html', d)


