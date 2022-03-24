import pyupbit
import datetime



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
    #코인 이름과 가격 딕셔너리 형태로 저장
    coinitem=""
    for i in range(len(coin)):
        if(coinname ==coin[i]):
            coinitem = coinlist[i]
        else:
            pass
    df = pyupbit.get_ohlcv(coinitem,interval="day",to = nowDATE,count = date)
    return df

#코인 이름 형식화 후 리스트로 저장 (여기서부터 수정해야함!!!)
def coin_rate(coinlist,moneyvalue,coinitem):
    nowDATE = time_format()
    coinrate =[]
    coinrate.append(nowDATE)
    for i in range(len(coin)):
        if(coinitem ==coin[i]):
            number = i
            coinrate.append(coin[number]+"("+moneyvalue+")")
        else:
            pass
    return coinrate

#코인 가격 형식화 후 리스트로 저장
def price_correct(coinlist,content):
    coinprice=[]
    for name in coinlist:
        if(content[name]>100):
            coinprice.append(format(int("{:.0f}".format(content[name])),',')+"원")
        else:
            coinprice.append("{:.2f}".format(content[name])+"원")
    return coinprice

def COIN_made(coinlist,content):
    COIN = {}
    #형식화된 코인 이름들 가져오기
    coinname = namecorrect(coinlist)
    #형식화된코인 가격들 가져오기
    coinprice = pricecorrect(coinlist, content)
    #딕셔너리 형태로 이름과 가격 저장
    for i in range(len(coinname)):
        COIN[coinname[i]]=coinprice[i]

    return COIN
#nowDate = time_format()
#df = pyupbit.get_ohlcv("KRW-BTC",interval="day",to = nowDate,count = 1065)
#print(df)
a,b = coin_connect("USD", "비트코인", 1065)