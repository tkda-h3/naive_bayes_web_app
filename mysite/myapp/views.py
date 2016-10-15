# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from . import forms


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def hello_forms(request):
    form = forms.HelloForm(request.GET or None)
    if form.is_valid():
        message = 'データ検証に成功しました'
    else:
        message = 'データ検証に失敗しました'
    d = {
        'form': form,
        'message': message,
    }
    return render(request, 'forms.html', d)


