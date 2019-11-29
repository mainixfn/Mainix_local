import datetime as dt
import json
from django.http import HttpResponse
from django.shortcuts import render
import requests
import sys
import os
from bs4 import BeautifulSoup
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainix.settings")
django.setup()
import schedule
import time
import pandas as pd
from pairtrade_stock.function import Kosdaq_Signals,Kospi_Signals,Pairtrade_dt ,stock_price
from pairtrade_stock.models import Stock_Table , Kospi_StockName , Kosdaq_StockName,Stock_Pair_Trade


top5_list=['베셀','케이피에스','아나패스','아이씨디', '엘티씨']
name1='힘스'
Pair_Data=Kosdaq_Signals(name1, top5_list)


def Kosdaq_Signal_db():
    n=len(Pair_Data)
    for i in range(n):
        d = Pair_Data[i]['Date']
        s1 = Pair_Data[i]['Stock1']
        s2 = Pair_Data[i]['Stock2']
        sig = Pair_Data[i]['Signal']
        Stock_Table(Date=d, Stock_Name1=s1, Stock_Name2=s2, Signal=sig).save()
    print('save')

