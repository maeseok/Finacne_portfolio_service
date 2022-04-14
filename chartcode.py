import pandas as pd
import requests
import pickle
#plt 관련해서 잘 모름 -> 공부 후 차트 수정 
# 필요한 모듈 import 하기 
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px
import datetime
import FinanceDataReader as fdr
import US
import pymongo
import PWD
pwd = PWD.pwd()
#한국 가격 형식화 함수
def KRX_rate(df_KRX,Name,date):
    nowDATE = US.time_format()
    #client = pymongo.MongoClient("mongodb+srv://maeseok:"+pwd+"@finance.smjhg.mongodb.net/data?retryWrites=true&w=majority")
    #KRX = client['KRX']
    #KRX.data.create_index('Name')
    #find 속도만 빨라지면 될듯.. + 차트가 느림
    #data = KRX.data.find_one({"Name":Name})
    #symbol = data.get("Symbol")
    symbol = df_KRX[df_KRX.Name==Name].Symbol.values[0].strip()
    df_rate = fdr.DataReader(symbol,date)
    rate = df_rate[['Close','Change']]
    KRXrate = rate[-2:]
    KRX = []
    KRX.append(nowDATE)
    KRX.append(Name)
    KRX.append('{0:,}'.format(KRXrate['Close'].values[1])+"원")
    gap = KRXrate['Close'].values[1]-KRXrate['Close'].values[0]
    KRX.append("{0:,}".format(gap) +"원")
    KRX.append(str("{:.2f}".format(KRXrate['Change'].values[1]*100))+'%')
    return KRX,symbol,df_rate

#한국 데이터 연결하는 함수
def KRX_connect():
    codepath = "./DBandDB_SOURCE/krx.txt"
    f = open(codepath,"r")
    df_krx = pd.read_pickle(codepath)
    f.close()
    return df_krx

#기본 차트 생성
def make_basic_chart(df,company):
    #차트크기
    plt.figure(figsize=(13,4))
    #차트 값 (x랑 y에 어떤 값 넣을지)
    plt.plot((df['date']), df['close'])
    #차트 행마다 이름
    plt.xlabel('Date')
    plt.ylabel('Close')
    #차트 옵션
    plt.tick_params(
        axis='both',     #x,y 축 틱 모두 적용
        which='both',    #틱에 인수를 적용
        bottom=False,    #아래 눈금선 없애기
        top=False,)      #위에 눈금선 없애기
    #차트 이미지로 저장
    src="./static/assets/img/"
    plt.savefig(src+company + ".png")

#한국 수익률 형식화 함수
def KRX_yield(df_KRX,Name,firstdate,lastdate):

    symbol = df_KRX[df_KRX.Name==Name].Symbol.values[0].strip()
    rate = fdr.DataReader(symbol,firstdate,lastdate)
    rate = rate[['Close']]
    Firstrate = rate['Close'].values[0]
    Lastrate = rate['Close'].values[-1]
    KRX = []
    KRX.append(firstdate+"\t"+ '{0:,}'.format(Firstrate)+"원")
    KRX.append(lastdate+"\t" + "{0:,}".format(Lastrate) +"원")
    KRXyield = (int(Lastrate)-int(Firstrate))/int(Firstrate)*100
    KRX.append(str("{:.2f}".format(KRXyield)+'%'))
    return KRX



#크롤링 코드 (사용 안 함)
def crawling_fun(company,code):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
    #df를 dataframe 형태로 생성
    df = pd.DataFrame()
    for page in range(1, 10):
        url = 'https://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
        url = '{url}&page={page}'.format(url=url, page=page)
        res = requests.get(url, headers = headers).text
        #html 형태로 url을 읽어들여서 df에 추가함
        df = df.append(pd.read_html(res, header=0)[0], ignore_index=True)
    #NAN 값이 있는 데이터 제거하기
    df = df.dropna()
    #한국 이름 영어 이름으로 바꾸기
    df = df.rename(columns= {'날짜': 'date', '종가' : 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가':'low','거래량':'volume'})
    #astype -> 데이터 프레임 형변환
    df[['close','diff','open','high','low','volume']] = df[['close','diff','open','high','low','volume']].astype(int)
    #int64 형태로 저장된 값을 datetime64 형태로 바꾸기
    df['date'] = pd.to_datetime(df['date'])
    #date 기준으로 오름차순으로 정렬하여 저장
    df = df.sort_values(by=['date'], ascending=True)
    return df
