# -*- coding: utf-8 -*-
from django import forms


class HelloForm(forms.Form):
    your_name = forms.CharField(
        label='name',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    
