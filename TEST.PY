import ccxt
import re 
import pandas as pd
import datetime
import pyupbit
import datetime

#아맥스 가격 생성하는 함수
def ETFUS_rate(df_etfus,Name):
    nowDATE = time_format()

    symbol = df_etfus[df_etfus.Name==Name].Symbol.values[0].strip()
    rate = fdr.DataReader(symbol,nowDATE[:7])
    rate = rate[['Close','Change']]
    etfusrate = rate[-2:]
    ETFUS = []
    ETFUS.append(nowDATE)
    ETFUS.append(Name)
    ETFUS.append('$ '+str(etfusrate['Close'].values[1]))
    gap = "{:.2f}".format(etfusrate['Close'].values[1]-etfusrate['Close'].values[0])
    ETFUS.append('$ '+gap)
    ETFUS.append(str("{:.2f}".format(etfusrate['Change'].values[1]*100))+'%')
    return ETFUS