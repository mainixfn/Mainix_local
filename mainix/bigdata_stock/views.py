import datetime as dt
import json
from django.http import HttpResponse
from django.shortcuts import render
import sys
import os
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "svcode.svcode.settings")
django.setup()
from stock_pair.models import Stock_Table,Stock_Pair_Trade

def Stock_index(request):
    context = {}
    Trade_data = Stock_Pair_Trade.objects.all()
    for i in range(len(top5_list)):
        name = top5_list[i]
        name = Trade_data.filter(Pair_stock=name)
        context[str(i) + '_dt'] = name
    return render(request,'Pair_stock_index.html',context)


def Data_Table(request):
    signals =  Stock_Table.objects.order_by('-Date')
    context ={'signals':signals}
    return render(request,'tables.html',context)

top5_list=['베셀','케이피에스','아나패스','아이씨디', '엘티씨']

def Trade_Profit(request):
    context={}
    Trade_data = Stock_Pair_Trade.objects.all()
    for i in range(len(top5_list)):
        name=top5_list[i]
        name=Trade_data.filter(Pair_stock=name)
        context[str(i) + '_dt']=name
    return render(request,'chart_base.html',context)



