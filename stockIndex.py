import FinanceDataReader as fdr
import pyupbit
#s&p500, kospi 가격
def index_made(symbol):
    df = fdr.DataReader(symbol,'2022')
    df.reset_index(inplace=True)
    df = df[['Close']]
    df = df[-2:]
    rate = "{0:,}".format(df['Close'].values[1])
    firstrate = df['Close'].values[0]
    lastrate = df['Close'].values[1]
    gap = "{0:,.0f}".format(lastrate-firstrate)
    profit = "{:.2f}".format((lastrate-firstrate)/firstrate*100) + "%"
    return rate, profit

#비트코인 가격 
def coin_index():
    #df에 해당 코인의 데이터를 저장
    df = pyupbit.get_ohlcv("KRW-BTC",interval="day",count = 2)
    df = df[['close']]
    df = df[-2:]
    rate = "{0:,.0f}".format(df['close'].values[1])
    firstrate = df['close'].values[0]
    lastrate = df['close'].values[1]
    gap = "{0:,.0f}".format(lastrate-firstrate)
    profit = "{:.2f}".format((lastrate-firstrate)/firstrate*100) + "%"
    return rate, profit
