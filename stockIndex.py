import FinanceDataReader as fdr
import pyupbit
import schedule
import time
#s&p500, kospi 가격
def index_made(symbol):
    df = fdr.DataReader(symbol,'2022')
    df.reset_index(inplace=True)
    df = df[['Close']]
    df = df[-2:]
    rate = "{0:,}".format(df['Close'].values[1])
    firstrate = df['Close'].values[0]
    print(firstrate)
    lastrate = df['Close'].values[1]
    gap = "{0:,.0f}".format(lastrate-firstrate)
    profit = "{:.2f}".format((lastrate-firstrate)/firstrate*100) + "%"
    post = {"Rate":rate,"Profit":profit}
    if(symbol == "KS11"):
        path = "./DB/INDEX/kospi.txt"
        f = open(path,"a")
        f.write(rate+"\n")
        f.write(profit+"\n")
        f.close()
    elif(symbol == "US500"):
        path = "./DB/INDEX/sp500.txt"
        f = open(path,"a")
        f.write(rate+"\n")
        f.write(profit+"\n")
        f.close()
    else:
        pass
#비트코인 가격 
def coin_index():
    #df에 해당 코인의 데이터를 저장
    df = pyupbit.get_ohlcv("KRW-BTC",interval="day",count = 2)
    df = df[['close']]
    df = df[-2:]
    rate = pyupbit.get_current_price(["KRW-BTC"])
    #rate = "{0:,.0f}".format(df['close'].values[1])
    firstrate = df['close'].values[0]
    lastrate = rate
    rate = "{0:,.0f}".format(rate)
    gap = "{0:,.0f}".format(lastrate-firstrate)
    profit = "{:.2f}".format((lastrate-firstrate)/firstrate*100) + "%"
    post = {"Rate":rate,"Profit":profit}

    path = "./DB/INDEX/coin.txt"
    f = open(path,"a")
    f.write(rate+"\n")
    f.write(profit+"\n")
    f.close()


schedule.every(1).minutes.do(index_made,"KS11")
schedule.every(1).minutes.do(index_made,"US500")
schedule.every(1).minutes.do(coin_index)

while True:
    schedule.run_pending()
    print("스케줄 실행 중!")
    time.sleep(2)


