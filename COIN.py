import pyupbit
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

#코인 이름 한글로 정리
coin = ["비트코인","이더리움","네오","메탈","라이트코인","리플","이더리움 클래식","오미세고",
"스테이터스네트워크토큰","웨이브","넴","퀸텀","리스크","스팀","스텔라루멘",
"아더","아크","스토리지","그로스톨코인","어거","에이다","스팀달러","파워렛저","비트코인 골드",
"아이콘","이오스","트론","시아코인","온톨로지","질리카","폴리매쓰","제로엑스","룸네트워크","비트코인 캐시",
"베이직어텐션토큰","아이오에스티","리퍼리움","시빅","에브리피디아","아이오타","메인프레임","온톨로지가스",
"가스","센티넬프로토콜","엘프","카이버네트워크","비트코인에스브이","쎄타토큰","쿼크체인","비트토렌트","모스",
"엔진","쎄타퓨엘","디센트럴랜드","앵커","아르고","코스모스","썬더토큰","캐리프로토콜","무비블록","왁스","헤데라",
"메디블록","밀크","에스티피","오브스","비체인","칠리즈","스톰엑스","디카르고","하이브","카바","아하토큰","링크","테조스",
"보라","저스트","크로노스","톤","스와이프","헌트","플레이댑","폴카닷","세럼","엠블","스트라티스","알파쿼크","골렘","썸씽","메타",
"피르마체인","코박 토큰","샌드박스","휴먼스케이프","도지","스트라이크","펀디엑스","플로우","던프로토콜","엑시","스택스","이캐시","솔라나",
"폴리곤","누사이퍼","에이브","1인치","알고랜드","니어프로토콜","위믹스","아발란체","티"]

#현재 시간 불러오는 함수
def time_format():
    try:
        now = datetime.datetime.now()
        nowDATE=now.strftime('%Y-%m-%d')
        return nowDATE
    except:
        print("알림 : <현재 시간을 불러오는 중 오류가 발생했습니다.")

#라이브러리 연결
def coin_connect(moneyvalue,coinname,date):
    #코인 리스트 가져오기(pyupbit)
    nowDATE = time_format()
    coinlist= pyupbit.get_tickers(fiat=moneyvalue)
    #한글로 입력 받은 코인 이름을 영어로 변경
    coinitem=""
    for i in range(len(coin)):
        if(coinname ==coin[i]):
            coinitem = coinlist[i]
        else:
            pass
    #df에 해당 코인의 데이터를 저장
    df = pyupbit.get_ohlcv(coinitem,interval="day",to = nowDATE,count = date)
    return df

#코인 가격 리스트에 저장
def coin_rate(moneyvalue,coinitem,df):
    nowDATE = time_format()
    #오픈 가격만 뒤에서 2줄만 가져옴
    df_coin = df[['open']]
    df_coin = df_coin[-2:]
    #해당 값을 두 개의 변수에 저장
    firstrate = df_coin['open'].values[0]
    lastrate = df_coin['open'].values[1]
    coinrate =[]
    #날짜와 코인 이름, 현재 가격을 추가
    coinrate.append(nowDATE)
    coinrate.append(coinitem+"("+moneyvalue+")")
    gap = "{0:,.0f}".format(lastrate-firstrate)
    if(moneyvalue == "KRW"):
         #변동 계산 및 추가
        coinrate.append("{0:,.0f}".format(lastrate)+"원")
        coinrate.append(gap+"원")
    elif(moneyvalue == "USD"):
         #변동 계산 및 추가
        coinrate.append("$"+"{0:,.0f}".format(lastrate))
        coinrate.append("$"+gap)
    #수익률 계산 및 추가
    profit = "{:.2f}".format((lastrate-firstrate)/firstrate*100)
    coinrate.append("{0:,}".format(float(profit))+"%")
    return coinrate

#기본 차트 만들기
def basic_chart(df,Name):
    #현재 인덱스인 값을 date라는 값으로 데이터프레임에 추가
    df['date'] = df.index
    #차트크기
    plt.figure(figsize=(13,4))
    #차트 값 (x랑 y에 어떤 값 넣을지)
    plt.plot(df['date'],df['open'])
    #차트 행마다 이름
    plt.xlabel('Date')
    plt.ylabel('Close')
    src="./static/assets/img/"
    plt.savefig(src+Name + ".png")
    
#내가 잘 모르는 내용
def real_chart(df,company):
    #고급 차트 생성
    fig = px.line(df, x='date', y='open', title='{}의 시가(Open) '.format(company))

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

