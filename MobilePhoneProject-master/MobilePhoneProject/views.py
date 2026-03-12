# D:\桌面\MobilePhoneProject\views.py
from django.shortcuts import render

def index(request):
    """自定义首页视图"""
    return render(request, 'register.html')