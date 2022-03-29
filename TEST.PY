import ccxt


#USD df 생성
def usd_made():
    exchange = ccxt.binance() #바이낸스 객체 생성
    exchange.fetch_tickers() #티커의 각종 정보를 딕셔너리로 불러옴 
    ticker = list(exchange.fetch_tickers().keys()) #딕셔너리의 key값만 뽑아내서 리스트로 만들
    USDT_ticker = [] 
    import re 
    p = re.compile(r'\w+[/]USDT')
    for i in ticker:
        if p.match(i) and 'UP' not in i and 'DOWN' not in i: #레버리지토큰 필터링을 위함
            USDT_ticker.append(i)
    print(USDT_ticker)

usd_made()