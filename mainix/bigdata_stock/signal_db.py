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
import schedule
import time
import pandas as pd
from stock_pair.function import Kosdaq_Signals,Kospi_Signals,Pairtrade_dt ,stock_price
from stock_pair.models import Stock_Table , Kospi_StockName , Kosdaq_StockName,Stock_Pair_Trade





time1 = dt.datetime.now()
nowtime = time1.strftime('%Y-%m-%d'+'T'+'%H')

days = 500

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





def Stock_Pair_Profit():
    top5_list = ['베셀', '케이피에스', '아나패스', '아이씨디', '엘티씨']
    name1 = '힘스'
    data_list={}
    Trade_data = Stock_Pair_Trade.objects.all()
    Signal_data = Stock_Table.objects.all()
    kosdaq_db = Kosdaq_StockName.objects.all()
    kosdaq_dic = {}
    position=[]
    for stock in kosdaq_db:
        s = stock.stock_name
        c = stock.stock_code
        kosdaq_dic[s] = c
    trade_num = 20
    for i in range(len(top5_list)):
        name = top5_list[i]
        base_data= Trade_data.filter(Pair_stock=name).last()
        signal_data = Signal_data.filter(Stock_Name2=name).last()
        data_list[name]={'profit': base_data.Cash_Balance, 'signal':signal_data.Signal,'c1':base_data.Count1,
                         'c2':base_data.Count2,'avg1' : base_data.Avg_price1,'avg2' : base_data.Avg_price2}

    for n in top5_list:
        money = data_list[n]['profit']
        countS1 = data_list[n]['c1']
        countS2 = data_list[n]['c2']
        signal = data_list[n]['signal']
        avg_p1 = data_list[n]['avg1']
        avg_p2 =  data_list[n]['avg2']
        code2 = kosdaq_dic[n]
        code1 = kosdaq_dic[name1]
        S1_price = stock_price(code1)['openPrice'][-1]
        S2_price = stock_price(code2)['openPrice'][-1]
        Date =time1.strftime('%Y-%m-%d')

        if signal == n + '매수':
            money += 0
            countS1 -= trade_num
            countS2 +=  (S1_price/S2_price)* trade_num
            avg_price1 = avg_p1
            avg_price2 = int((S2_price + avg_p2)/2)
            assesment = money + int(countS2*S2_price*(S2_price/avg_price2-1))
            position.append(
                {'Date': Date, '수익': money, name1: countS1, n : countS2, '평가수익': assesment,  "avg_price1":avg_price1,'avg_price2': avg_price2})
        elif signal == name1 + '매수':
            money -= 0
            countS1 += trade_num
            countS2 -=(S1_price/S2_price) * trade_num
            avg_price1 = int((S1_price + avg_p1) / 2)
            avg_price2 = avg_p2
            assesment = money + int(countS1*S1_price*(S1_price/avg_price1-1))
            position.append(
                {'Date': Date, '수익': money, name1: countS1, n: countS2, '평가수익': assesment, "avg_price1": avg_price1,
                 'avg_price2': avg_price2})

            # Clear positions if the z-score between -.5 and .5
            # -0.5~0.5 사이인 경우 수익일 경우 이익 실현
        elif signal=='청산':
            if countS1 > 0:
                money += int(countS1*S1_price - countS1*avg_p1)
            elif countS2 > 0:
                money += int(countS2*S2_price - countS2*avg_p2)
            else:
                pass
            countS1 = 0
            countS2 = 0
            # total = money + Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2

            position.append(
                {'Date': Date, '수익': money, name1: countS1, n: countS2, '평가수익': money,"avg_price1": 0,'avg_price2': 0})
        else:
            position.append(
                    {'Date': Date, '수익': money, name1: countS1, n: countS2, '평가수익': money,"avg_price1": avg_p1, 'avg_price2': avg_p2})

        d = Date
        s1 = name1
        s2 = n
        pro = money
        p1 = countS1
        p2 = countS2
        av1 = avg_p1
        av2 = avg_p2
        Stock_Pair_Trade(Date=d, Base_stock=s1, Pair_stock=s2, Cash_Balance=pro, Count1=p1, Count2=p2, Avg_price1=av1,
                         Avg_price2=av2).save()
        print('save')


schedule.every(10).seconds.do(Kosdaq_Signal_db)
while True:
    schedule.run_pending()
    time.sleep(1)
#schedule.every(10).seconds.do(Stock_Pair_Profit)
#schedule.every(10).seconds.do(Kosdaq_Signal_db)
#schedule.every(60).seconds.do(Kosdaq_Signal_db)
#print(Kosdaq_Signal_db())

'''
schedule.every().day.at("00:30").do(Kosdaq_Signal_db)
schedule.every().day.at("09:30").do(Stock_Pair_Profit) #매십포마다 실행


while True:
    schedule.run_pending()
    time.sleep(1)
'''


















'''
def Kosdaq_trade_db():
    kosdaq_db = Kosdaq_StockName.objects.all()
    kosdaq_dic = {}
    for stock in kosdaq_db:
        s = stock.stock_name
        c = stock.stock_code
        kosdaq_dic[s] = c
    pair_signals = []
    for i in range(len(top5_list)):
        name2 = top5_list[i]
        Total_StockNmae_dic = kosdaq_dic
        window1 = 5
        window2 = 60
        code1 = Total_StockNmae_dic[name1]
        code2 = Total_StockNmae_dic[name2]
        S1 = stock_price(code1)
        S2 = stock_price(code2)
        ratios = S1.div(S2)
        S1 = S1.rename(columns={'openPrice': name1})
        S2 = S2.rename(columns={'openPrice': name2})
        ratios = ratios.rename(columns={'openPrice': 'ratios'})
        ratios = ratios.dropna()
        ma1 = ratios.rolling(window=window1,
                             center=False).mean()
        ma2 = ratios.rolling(window=window2,
                             center=False).mean()
        std = ratios.rolling(window=window2,
                             center=False).std()
        zscore = (ma1 - ma2) / std
        # zscore = zscore[window2-1:]
        zscore = zscore.rename(columns={'ratios': 'zscore'})
        Price_ratios = pd.concat([S1, S2, ratios, zscore], axis=1, sort=True)
        Price_ratios = Price_ratios.dropna()
        def Pairtrade_dt(Price_ratios):
            money = 0
            countS1 = 0
            countS2 = 0
            position = []
            trade_num = 20

            # print(Price_ratios['zscore'])
            S1_price = []
            S2_price = []

            for i in range(len(Price_ratios)):
                # Sell short if the z-score is > 1
                Date = Price_ratios.index[i]
                if i > 1:
                    avg_price2 = 0
                    avg_price1 = 0
                    if Price_ratios['zscore'].values[i - 1] > 1:
                        money += 0
                        countS1 -= trade_num
                        countS2 += Price_ratios['ratios'][i] * trade_num
                        S2_price.append(Price_ratios[name2][i])
                        # assessment =
                        # total = money + Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2
                        avg_price2 = int(sum(S2_price)/len(S2_price))
                        assesment = money + int(countS2 * (sum(S2_price) / len(S2_price)) * (Price_ratios[name2][i] / (sum(S2_price) / len(S2_price)) - 1))
                        position.append(
                            {'Date': Date, 'signal': round(Price_ratios['zscore'].values[i], 3), 'postion': '매도',
                             '수익': money, name1: countS1,
                             name2: countS2, '평가수익': assesment, "avg_price1":avg_price1,'avg_price2': avg_price2})
                    elif Price_ratios['zscore'].values[i - 1] < -1:
                        money -= 0
                        countS1 += trade_num
                        countS2 -= Price_ratios['ratios'][i] * trade_num
                        S1_price.append(Price_ratios[name1][i])
                        # total = money + Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2
                        avg_price1 = int(sum(S1_price)/len(S1_price))
                        assesment = money + int(countS1 * (sum(S1_price) / len(S1_price)) * (
                                    Price_ratios[name1][i] / (sum(S1_price) / len(S1_price)) - 1))
                        position.append(
                            {'Date': Date, 'signal': round(Price_ratios['zscore'].values[i], 3), 'postion': '매수',
                             '수익': money, name1: countS1,
                             name2: countS2, '평가수익': assesment,  "avg_price1":avg_price1,'avg_price2': avg_price2})

                    # Clear positions if the z-score between -.5 and .5
                    # -0.5~0.5 사이인 경우 수익일 경우 이익 실현
                    elif abs(Price_ratios['zscore'].values[i - 1]) < 0.4 and (Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2) > 0:
                        if countS1 > 0:
                            money += int(countS1 * (sum(S1_price) / len(S1_price)) * (
                                        Price_ratios[name1][i] / (sum(S1_price) / len(S1_price)) - 1))
                        elif countS2 > 0:
                            money += int(countS2 * (sum(S2_price) / len(S2_price)) * (
                                        Price_ratios[name2][i] / (sum(S2_price) / len(S2_price)) - 1))
                        else:
                            pass
                        countS1 = 0
                        countS2 = 0
                        # total = money + Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2

                        position.append(
                            {'Date': Date, 'signal': round(Price_ratios['zscore'].values[i], 3), 'postion': '청산',
                             '수익': money, name1: countS1,name2: countS2, '평가수익': money,  "avg_price1":avg_price1,'avg_price2': avg_price2})
                        S1_price.clear()
                        S2_price.clear()
                    else:
                        if len(position)>0:
                            position.append({'Date': Date, 'signal': round(Price_ratios['zscore'].values[i], 3), 'postion': '대기',
                                 '수익': money, name1: countS1,name2: countS2, '평가수익': position[-1]['평가수익'],  "avg_price1":avg_price1,'avg_price2': avg_price2})
                        else:
                            position.append(
                                {'Date': Date, 'signal': round(Price_ratios['zscore'].values[i], 3), 'postion': '대기',
                                 '수익': money, name1: countS1, name2: countS2, '평가수익': 0, "avg_price1":avg_price1,'avg_price2': avg_price2})

                else:
                    pass
            return position
        Trade_Data = Pairtrade_dt(Price_ratios)

        n = len(Trade_Data)

        for i in range(n):
            d = Trade_Data[i]['Date']
            s1 = name1
            s2 = name2
            pro = Trade_Data[i]['평가수익']
            p1=Trade_Data[i][name1]
            p2=Trade_Data[i][name2]
            av1 =Trade_Data[i]['avg_price1']
            av2 =Trade_Data[i]['avg_price2']
            Stock_Pair_Trade(Date=d, Base_stock=s1, Pair_stock=s2,Cash_Balance=pro ,Count1=p1,Count2=p2,Avg_price1=av1,Avg_price2=av2).save()
        print(Trade_Data)
        print('save')

#print(Kosdaq_trade_db())
'''
