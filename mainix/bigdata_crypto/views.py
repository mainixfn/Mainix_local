from django.http import HttpResponse
from django.shortcuts import render
import json
import sys
import os
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainix.settings")
django.setup()
from bigdata_crypto.function import H_Signals
from bigdata_crypto.models import Tredn_Sig_Table

def sig_index(request):
    signals = Tredn_Sig_Table.objects.order_by('-Date')[:20]
    context = {'signals': signals}
    return render(request,'trend_crypto_index.html',context)

def Data_Table(request):
    signals = Tredn_Sig_Table.objects.order_by('-Date')[:20]
    context = {'signals': signals}
    return render(request,'Trend_table.html',context)



