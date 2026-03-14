from django.shortcuts import render


def index(request):
    """自定义首页视图"""
    return render(request, '../static/register.html')
