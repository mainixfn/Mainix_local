from pytrends.request import TrendReq
from pandas import DataFrame
import requests
import pandas as pd
import math
import sys
import os
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainix.settings")
django.setup()
import time
from bigdata_crypto.models import Tredn_Sig_Table






coinNames = ['ATOM', 'XEM', 'BAT', 'BSV', 'ETH', 'XLM', 'BTC',
             'DCR', 'ADA', 'ETC', 'XMR', 'ONT', 'XRP', 'TRX', 'BCH', 'EOS', 'ZEC', 'NEO', 'DASH', 'LTC']
#가격함수

def H_Price(coinName):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    count = "168";  # 기간
    url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/60?code=CRIX.UPBIT.KRW-' + coinName + '&count=' + count + '';

    res = requests.get(url, headers=headers)
    data = res.json()
    upbit_prices = []
    price_date = []
    data.reverse()
    #data2 = data[1]["tradePrice"]
    #date = data[1]["candleDateTime"]

    for a in range(len(data)):
        data1 = data[a]['tradePrice']
        upbit_prices.append(data1)

    for i in range(len(data)):
        date = data[i]["candleDateTime"]
        date = date.split('+')
        del date[1]
        date = date[0]
        price_date.append(date)

    price_df = DataFrame({"price": upbit_prices}, index=price_date)
    return price_df

BTC_price_df = H_Price('BTC')

def BTC_Signals():
    # BTC 트랜드 시그널 생성
    Period = 2;
    BTC_signals = []
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = ["Bitcoin"]  # 키워드 설정
    pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='US', gprop='')  # 트랜드 기간 설정 , 지역설정, 예외설정
    cointrenddf = pytrends.interest_over_time()
    trends_df = cointrenddf["Bitcoin"]  # Bitcoin 트랜트만
    trends_dfma5 = trends_df.rolling(window=Period).mean()  # Bitcoin 트랜드 기간평균

    trends_df = trends_df.iloc[1:]  # 트랜드의 초기값 삭제
    trends_dfma5 = trends_dfma5.iloc[:-1]  # 기간평균의 마지막값 삭제

    for trd, ma5 in zip(trends_df, trends_dfma5):
        if ma5 == 0:
            BTC_signals.append('None')
        else:
            BTC_signals.append(trd - ma5)
    return  BTC_signals
 # 코인별 신호갑 부여 함수

def H_Signals() :
    statecont =1
    signals_list = []
    signals = BTC_Signals()
    BTC_price_df = H_Price('BTC')
    error0001=["0001Error"]
    for coinName in coinNames:
        try:
            price = H_Price(coinName)
            def Corr(coinName):
                Alt_price_df =price
                Total_Price_df = pd.concat([Alt_price_df, BTC_price_df], axis=1, sort=True)
                corr_value = Total_Price_df.corr(method='pearson')
                return corr_value.values[0][1]

            if -0.2 < Corr(coinName) < 0.2:
                corr = 1
            else:
                corr = Corr(coinName)
            corr_signals = signals[-2] * (1 /corr)  # 코인별 상관계수 부여
            corr_signals = round(corr_signals,3)
            corr_signals = corr_signals * statecont
            corr_signaled = signals[-4]*(1/corr)*statecont
            if corr_signaled > 0:
                profit = math.log((price['price'][-2] / price['price'][-4])) * 100
            else:
                profit = math.log((price['price'][-4] / price['price'][-2])) * 100
            if abs(168 - len(pd.concat([price,BTC_price_df], axis=1, sort=True))) < 30:
                status = "0000"
                last_price = price['price'][-2]
                last_profit = profit
                corr_signals = corr_signals
            else:
                status = "0001"
                last_price = "Nan"
                last_profit = "Nan"
                corr_signals = "Nan"
                error0001.append(coinName)

            signals_list.append({"Status":status,"Date": price.index[-1] + "+" "09:00:00""KST", "Price": last_price,
                 "CoinName": coinName, "Signal": corr_signals, "Profit":last_profit})


        except:
            signals_list.append({"Status":"0010","Date": price.index[-1] + "+" "09:00:00KST","Price":"Nan",
                                 "CoinName":coinName,"Signal":"Nan","Profit":"Nan"})


    return signals_list


if __name__=='__main__':
    print(H_Signals())




'''
#request 받아 json으로 전송
def Signals(request) :
    signals_list = ["Trend Signal Data"]
    signals = BTC_Signals()
    BTC_price_df = H_Price('BTC')
    error0001=["0001Error"]
    for coinName in coinNames:
        try:
            price = H_Price(coinName)
            def Corr(coinName):
                Alt_price_df =price
                Total_Price_df = pd.concat([Alt_price_df, BTC_price_df], axis=1, sort=True)
                corr_value = Total_Price_df.corr(method='pearson')
                return corr_value.values[0][1]

            if -0.2 < Corr(coinName) < 0.2:
                corr = 1
            else:
                corr = Corr(coinName)
            corr_signals = signals[-2] * (1 /corr)  # 코인별 상관계수 부여
            corr_signals = round(corr_signals,3)
            corr_signals = corr_signals * statecont
            corr_signaled = signals[-4]*(1/corr)*statecont
            if corr_signaled > 0:
                profit = math.log((price['price'][-2] / price['price'][-4])) * 100
            else:
                profit = math.log((price['price'][-4] / price['price'][-2])) * 100
            if abs(168 - len(pd.concat([price,BTC_price_df], axis=1, sort=True))) < 30:
                status = "0000"
                last_price = price['price'][-2]
                last_profit = profit
                corr_signals = corr_signals
            else:
                status = "0001"
                last_price = "Nan"
                last_profit = "Nan"
                corr_signals = "Nan"
                error0001.append(coinName)

            signals_list.append({"Status":status,"Date": price.index[-1] + "+" "09:00:00""KST", "Price": last_price,
                 "CoinName": coinName, "Signal": corr_signals, "Profit":last_profit})


        except:
            signals_list.append({"Status":"0010","Date": price.index[-1] + "+" "09:00:00KST","Price":"Nan",
                                 "CoinName":coinName,"Signal":"Nan","Profit":"Nan"})

    signals_list.append(error0001)
    j_signals_list = json.dumps(signals_list,ensure_ascii = False)
    #return signals_list
    return  HttpResponse(j_signals_list, content_type='application/json')
'''