# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 21:39:28 2011

@author: ontiyonke
"""

from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField(label='Google E-mail')
    password = forms.CharField(label='Google Password', widget = forms.PasswordInput())