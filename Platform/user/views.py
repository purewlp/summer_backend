from django.shortcuts import render
from django.http import JsonResponse
from Platform import settings
# Create your views here.

def test(request):
    if request.method=='POST':
        return JsonResponse({'errno':0,'msg':"测试成功"})
    else:
        return JsonResponse({'errno':1001,'msg':"测试失败"})