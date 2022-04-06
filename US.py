import FinanceDataReader as fdr
import datetime
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#현재 시간 불러오는 함수
def time_format():
    try:
        now = datetime.datetime.now()
        nowDATE=now.strftime('%Y-%m-%d')
        return nowDATE
    except:
        print("알림 : <현재 시간을 불러오는 중 오류가 발생했습니다.")

#나스닥 가격 생성하는 함수
def NASDAQ_rate(df_nasdaq,Name):
    nowDATE = time_format()

    symbol = df_nasdaq[df_nasdaq.Name==Name].Symbol.values[0].strip()
    rate = fdr.DataReader(symbol,nowDATE[:7])
    rate = rate[['Close','Change']]
    nasdaqrate = rate[-2:]
    NASDAQ = []
    NASDAQ.append(nowDATE)
    NASDAQ.append(Name)
    NASDAQ.append('$ '+str(nasdaqrate['Close'].values[1]))
    gap = "{:.2f}".format(nasdaqrate['Close'].values[1]-nasdaqrate['Close'].values[0])
    NASDAQ.append('$ '+gap)
    NASDAQ.append(str("{:.2f}".format(nasdaqrate['Change'].values[1]*100))+'%')
    return NASDAQ
#나스닥 데이터 연결하는 함수
def NASDAQ_connect():
    codepath = "./DBandDB_SOURCE/nasdaq.txt"
    f = open(codepath,"r")
    df_nasdaq = pd.read_pickle(codepath)
    f.close()
    return df_nasdaq

#뉴욕 증권거래소 가격 생성하는 함수
def NYSE_rate(df_nyse,Name):
    nowDATE = time_format()

    symbol = df_nyse[df_nyse.Name==Name].Symbol.values[0].strip()
    rate = fdr.DataReader(symbol,nowDATE[:7])
    rate = rate[['Close','Change']]
    nyserate = rate[-2:]
    NYSE = []
    NYSE.append(nowDATE)
    NYSE.append(Name)
    NYSE.append('$ '+str(nyserate['Close'].values[1]))
    gap = "{:.2f}".format(nyserate['Close'].values[1]-nyserate['Close'].values[0])
    NYSE.append('$ '+gap)
    NYSE.append(str("{:.2f}".format(nyserate['Change'].values[1]*100))+'%')
    return NYSE
#뉴욕 증권거래소 연결하는 함수
def NYSE_connect():
    codepath = "./DBandDB_SOURCE/nyse.txt"
    f = open(codepath,"r")
    df_nyse = pd.read_pickle(codepath)
    f.close()
    return df_nyse

#아맥스 가격 생성하는 함수
def AMEX_rate(df_amex,Name):
    nowDATE = time_format()

    symbol = df_amex[df_amex.Name==Name].Symbol.values[0].strip()
    rate = fdr.DataReader(symbol,nowDATE[:7])
    rate = rate[['Close','Change']]
    amexrate = rate[-2:]
    AMEX = []
    AMEX.append(nowDATE)
    AMEX.append(Name)
    AMEX.append('$ '+str(amexrate['Close'].values[1]))
    gap = "{:.2f}".format(amexrate['Close'].values[1]-amexrate['Close'].values[0])
    AMEX.append('$ '+gap)
    AMEX.append(str("{:.2f}".format(amexrate['Change'].values[1]*100))+'%')
    return AMEX
#아맥스 연결하는 함수
def AMEX_connect():
    codepath = "./DBandDB_SOURCE/amex.txt"
    f = open(codepath,"r")
    df_amex = pd.read_pickle(codepath)
    f.close()
    return df_amex
#ETF/US 가격 생성하는 함수
def ETFUS_rate(df_etfus,Name,company):
    nowDATE = time_format()

    symbol = df_etfus[df_etfus.Name==Name].Symbol.values[0].strip()
    rate = fdr.DataReader(symbol,nowDATE[:7])
    rate = rate[['Close','Change']]
    etfusrate = rate[-2:]
    ETFUS = []
    ETFUS.append(nowDATE)
    ETFUS.append(company)
    ETFUS.append('$ '+str(etfusrate['Close'].values[1]))
    gap = "{:.2f}".format(etfusrate['Close'].values[1]-etfusrate['Close'].values[0])
    ETFUS.append('$ '+gap)
    ETFUS.append(str("{:.2f}".format(etfusrate['Change'].values[1]*100))+'%')
    return ETFUS

#ETF/US 연결하는 함수
def ETFUS_connect():
    codepath = "./DBandDB_SOURCE/etfus.txt"
    f = open(codepath,"r")
    df_etfus = pd.read_pickle(codepath)
    f.close()
    return df_etfus

#정리된 df 만들기!
def df_made(Code,Name,Date):
    symbol = Code[Code.Name==Name].Symbol.values[0].strip()
    #이 값을 바꾸면 언제부터 시작할지도!(차트)
    df = fdr.DataReader(symbol,Date)
    #중요! Date를 index에서 제외시킨다!!!! -> df 자체를 정렬된 상태로 저장
    df.reset_index(inplace=True)
    df = df[['Date','Close']]
    return df

#기본 차트 만들기
def basic_chart(df,Name):
    #차트크기
    plt.figure(figsize=(13,4))
    #차트 값 (x랑 y에 어떤 값 넣을지)
    plt.plot(df['Date'],df['Close'])
    #차트 행마다 이름
    plt.xlabel('Date')
    plt.ylabel('Close')
    src="./static/assets/img/"
    plt.savefig(src+Name + ".png")

#내가 잘 모르는 내용
def real_chart(df,company):
    #고급 차트 생성
    fig = px.line(df, x='Date', y='Close', title='{}의 종가(Close) '.format(company))

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.write_html("./templates/chart.html")