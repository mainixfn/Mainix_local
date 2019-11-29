import sys
import os
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainix.settings")
django.setup()
import schedule
import time
from bigdata_crypto.function import H_Signals
from bigdata_crypto.models import Tredn_Sig_Table


def Trend_Coin_Signal_db():
    Pair_Data=H_Signals()
    n=len(Pair_Data)
    for i in range(n):
        d = Pair_Data[i]['Date']
        s1 = Pair_Data[i]['CoinName']
        sig = Pair_Data[i]['Signal']
        p = Pair_Data[i]['Price']
        pro = Pair_Data[i]['Profit']
        Tredn_Sig_Table(Date=d, CoinName=s1, Price=p, Signal=sig ,Profit=pro).save()
    print('save')

print(Trend_Coin_Signal_db())