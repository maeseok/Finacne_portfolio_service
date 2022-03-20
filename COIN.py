import pyupbit

#라이브러리 연결
def coin_connect():
    #코인 리스트 가져오기(pyupbit)
    coinlist= pyupbit.get_tickers(fiat='KRW')
    #코인 이름과 가격 딕셔너리 형태로 저장
    content = pyupbit.get_current_price(coinlist)

    return coinlist,content

#코인 이름 형식화 후 리스트로 저장
def name_correct(coinlist):
    coinname =[]
    for i in range(len(coinlist)):
        coinname.append(coinlist[i].replace("KRW-",""))
    return coinname

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
