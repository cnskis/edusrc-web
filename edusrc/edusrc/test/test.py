from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse('Hello,welcome to MXPY\'s Django project.')

def error(request,exception=404):#Django新版本需要加上exception
    return render(request,'hack.html',status=404)