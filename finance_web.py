from bs4 import BeautifulSoup
import urllib.request as req
import requests
from datetime import timedelta, datetime
from flask import Flask, render_template,request,redirect,flash,session,url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
#내가 만든 모듈
from basic import db_connect,only_code_made, time_format
from inquiry import stock_inquiry, rate_import
import portfolio as p
import chartcode as c
import COIN
import US
import db
import sys
import PWD

#로그 관리 
import logging
logging.basicConfig(filename = "./logs/test.log", level = logging.DEBUG)
nowDATE = time_format()
pwd = PWD.pwd()
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://maeseok:"+pwd+"@finance.smjhg.mongodb.net/members?retryWrites=true&w=majority"
app.config["SECRET_KEY"] = "bvWjJlEvRqsOBPnu"
app.config["PERMANET_SESSION_LIFETIME"] = timedelta(minutes = 30)
mongo = PyMongo(app)
#대표 화면
@app.route("/main")
def home():  
    #이건 DB도 옮기자! CRON까지 이용하면 좋을듯
    #결국 이 함수때문에 늦음 -> 한계인가?
    coinRate,coinProfit,sp500Rate,sp500Profit,kospiRate,kospiProfit = db.inquiry_index()
    return render_template("index.html",kospiRate = kospiRate, sp500Rate = sp500Rate, kospiProfit = kospiProfit,sp500Profit = sp500Profit,
    coinRate = coinRate, coinProfit = coinProfit)

@app.route("/")
def main():
    return render_template("main.html")
@app.route("/new",methods=["GET","POST"])
def new():
    if request.method == "POST":
        ID = request.form.get("id",type=str)
        pwd = request.form.get("pwd",type=str)
        pwd2 = request.form.get("pwd2",type=str)
        if id=="" or pwd=="" or pwd2=="":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("new.html") 
        if pwd!=pwd2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("new.html") 
        members = mongo.db.members
        data = members.find_one({"id":ID})
        if data is not None:
            flash("아이디가 중복됩니다.")
            return render_template("new.html") 

        post={
            "id":ID,
            "password": generate_password_hash(pwd),
            "logintime":"",
            "logincount":0,
        }

        members.insert_one(post)
        flash("회원가입이 완료되었습니다.")
        return render_template("login.html")
    else:
        return render_template("new.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        ID = request.form.get("id",type=str)
        pwd = request.form.get("pwd",type=str)
        members = mongo.db.members
        #members.create_index("id")
        data = members.find_one({"id":ID})
        if data is None:
            flash("회원정보가 없습니다.")
            return redirect(url_for("login"))
        else:
            if check_password_hash(data.get("password"),pwd):
                session["ID"] = str(data.get("id"))
                session.permenent = True
                flash("로그인 성공!")
                return redirect(url_for("home"))
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("login.html")
    else:
        return redirect(url_for("main"))
@app.route('/logout')
def logout():
    session.pop('ID', None)
    flash("로그아웃 성공!")
    return redirect('/main')
#포트폴리오 이용 설명
@app.route("/port_explain")
def port_explain():
    return render_template("port_explain.html")
#시세 조회
@app.route("/inquiry")
def inquiry():
    return render_template("inquiry.html")
#코인 시세 검색
@app.route("/inquiry/coin")
def coininquiry():
    return render_template("inquiryCoin.html")
#코인 시세 결과
@app.route("/inquiry/coinrate")
def coinreturn():
    try:
        moneyvalue = request.args.get('moneyValue')
        coinname = request.args.get('coinname')
        if(moneyvalue== "KRW"):
            df_coin,rate= COIN.coin_connect(moneyvalue,coinname,500)
            coinrate = COIN.coin_rate(moneyvalue,coinname,df_coin,rate)
        elif(moneyvalue == "USD"):
            ticker = COIN.usd_connect(coinname)
            df_coin = COIN.get_df_binance(ticker, "1d")
            coinrate = COIN.coin_rate(moneyvalue, coinname, df_coin)
        COIN.basic_chart(df_coin, coinname,moneyvalue)
        COIN.real_chart(df_coin,coinname)
    except:
        return redirect("/")
    return render_template("inquiryCoinrate.html",searchingBy=coinname,stockRate=coinrate)
#포트폴리오 
@app.route("/portfolio")
def portfolio():
    try:
        if(session['ID']):
            return render_template("portfolio.html")
    except:
        flash("로그인을 먼저 해주세요.")
        return render_template("login.html")
#코스피 코스닥 오늘의 종목 검색
@app.route("/inquiry/search")
def inquirySearch():
    return render_template("inquirySearch.html")
#코스피 코스닥 오늘의 시세 출력
@app.route("/inquiry/todayrate")
def inquiryTodayrate():
    try:
        company = request.args.get('company')
        date = request.args.get('date')
        df_krx = c.KRX_connect()
        stock_rate,symbol,df= c.KRX_rate(df_krx,company,date)
        df.reset_index(inplace=True)
        #chart img
        US.basic_chart(df,company)
        #chart html
        US.real_chart(df,company)
    except:
        return redirect("/")
    return render_template("inquiryTodayrate.html",searchingBy=company,stockRate=stock_rate)

#나스닥 오늘의 종목 검색
@app.route("/inquiry/nasdaq")
def NasdaqSearch():
    return render_template("inquiryNasdaq.html")
#나스닥 오늘의 시세 출력
@app.route("/inquiry/nasdaqrate")
def NasdaqRate():
    try:
        company = request.args.get('company')
        date = request.args.get('date')
        df_nasdaq = US.NASDAQ_connect()
        stock_rate,symbol = US.NASDAQ_rate(df_nasdaq,company)
        df = US.df_made(symbol,date)
        #chart img
        US.basic_chart(df,company)
        #chart html
        US.real_chart(df,company)
    except:
        return redirect("/")
    return render_template("inquiryNasdaqrate.html",searchingBy=company,stockRate=stock_rate)

#뉴욕 증권거래소 오늘의 종목 검색
@app.route("/inquiry/nyse")
def NyseSearch():
    return render_template("inquiryNyse.html")
#뉴욕 증권거래소 오늘의 시세 출력
@app.route("/inquiry/nyserate")
def NyseRate():
    #try:
    company = request.args.get('company')
    date = request.args.get('date')
    df_nyse = US.NYSE_connect()
    stock_rate,symbol = US.NYSE_rate(df_nyse,company)
    df = US.df_made(symbol,date)
    #chart img
    US.basic_chart(df,company)
    #chart html
    US.real_chart(df,company)
    #except:
        #return redirect("/")
    return render_template("inquiryNyserate.html",searchingBy=company,stockRate=stock_rate)

#아맥스 종목 검색
@app.route("/inquiry/amex")
def AmexSearch():
    return render_template("inquiryAmex.html")
#아맥스 오늘의 시세 출력
@app.route("/inquiry/amexrate")
def AmexRate():
    try:
        company = request.args.get('company')
        date = request.args.get('date')
        df_amex = US.AMEX_connect()
        stock_rate,symbol = US.AMEX_rate(df_amex,company)
        df = US.df_made(symbol,date)
        #chart img
        US.basic_chart(df,company)
        #chart html
        US.real_chart(df,company)
    except:
        return redirect("/")
    return render_template("inquiryAmexrate.html",searchingBy=company,stockRate=stock_rate)

#미국 ETF 종목 검색
@app.route("/inquiry/etfUS")
def EtfUS():
    return render_template("inquiryEtfUS.html")

#미국 ETF 오늘의 시세 출력
@app.route("/inquiry/etfUSrate")
def EtfUSrate():
    try:
        company = request.args.get('company')
        date = request.args.get('date')
        name = ""
        for i in range(len(company)):
            if company[i] == "[":
                name = company[:i]
        df_etfus = US.ETFUS_connect()
        stock_rate,symbol = US.ETFUS_rate(df_etfus,name,company)
        df = US.df_made(symbol,date)
        #chart img
        US.basic_chart(df,name)
        #chart html
        US.real_chart(df,name)
    except:
        return redirect("/")
    return render_template("inquiryEtfUSrate.html",searchingBy=name,stockRate=stock_rate)

#고급 차트 출력
@app.route("/chart")
def stockchart():
    return render_template("chart.html")

#종목 수익률 검색
@app.route("/inquiry/return")
def inquiryReturn():
    return render_template("inquiryReturn.html")

#종목 수익률 출력
@app.route("/inquiry/stock_return")
def stock_return():
    try:
        stocks = request.args.get('stocks')
        firstdate = request.args.get('purchase_date')
        lastdate = request.args.get('sale_date')
        df_krx = c.KRX_connect()
        KRX = c.KRX_yield(df_krx, stocks, firstdate, lastdate)
        return render_template("inquiryStock_return.html",KRX=KRX)
    except:
        return redirect("/")

#종목 매수 정보 입력
@app.route("/portfolio/buy")
def portfolioBuy():
    try:
        if(session['ID']):
            return render_template("portfolioBuy.html")
    except:
        flash("로그인을 먼저 해주세요.")
        return render_template("login.html")

#매수 완료 처리
@app.route("/portfolio/buy_return")
def portfolioBuy_return():
    if(session['ID']):
        pass
    else:
        flash("로그인을 먼저 해주세요.")
        return render_template("login.html")
    get_buycollect = p.buy_open()
    name = request.args.get('name')
    moneyvalue = request.args.get('moneyValue')
    path="/nomadcoders/boot/DB/check.txt"
    file = open(path, 'a')
    global checkCode
    checkCode="0"
    df_krx = c.KRX_connect()
    symbol = df_krx[df_krx.Name==name].Symbol.values[0].strip()
    name = name + moneyvalue
    print(name)
    if symbol:
        price = request.args.get('price')
        number = request.args.get('number')
        #이미 매수한 종목인지 확인
        if(name in get_buycollect):
            #매수한 경우 원래 값 수정
            p.buy_correct(name, price, number, get_buycollect)
            checkCode ="1"
        else:
            #새로 저장
            if(symbol):
                p.buy_save(name, price, number)
                checkCode ="2"
            else:
                checkCode="3"
    else:
        return redirect("/portfolio")
    file.write(checkCode)
    file.close()
    return render_template("portfolioBuy_return.html")


#종목 매수 완료
@app.route("/portfolio/buyreturn")
def BuyReturn():
    try:
        if(session['ID']):
            pass
        else:
            flash("로그인을 먼저 해주세요.")
            return render_template("login.html")
        path="/nomadcoders/boot/DB/check.txt"
        file = open(path, 'r')
        Check=int(file.read())
        file.close()
        file2 = open(path, 'w')
        file2.close()
        if(Check!=0):
            pass
        else:
            return redirect("/portfolio")
    except:
        return redirect("/portfolio")
    return render_template("portfolioBuyReturn.html",check=Check)

#종목 매도 정보 입력
@app.route("/portfolio/sell")
def portfolioSell():
    try:
        if(session['ID']):
            return render_template("portfolioSell.html")
    except:
        flash("로그인을 먼저 해주세요.")
        return render_template("login.html")

#종목 매도 처리
@app.route("/portfolio/sell_return")
def portfolioSell_return():
    try:
        try:
            if(session['ID']):
                pass
        except:
            flash("로그인을 먼저 해주세요.")
            return render_template("login.html")
        buycollect = p.buy_open()
        sellname = request.args.get('name2')
        sellprice = request.args.get('price2')
        sellnumber = request.args.get('number2')
        moneyvalue = request.args.get('moneyValue')
        check = "0"
        path="/nomadcoders/boot/DB/check.txt"
        checkcode = ""
        file = open(path, 'a')
        df_krx = c.KRX_connect()
        symbol = df_krx[df_krx.Name==sellname].Symbol.values[0].strip()
        if symbol:
            for i in range(0,len(buycollect)):
                if(buycollect[i] == sellname):
                    saveprice = buycollect[i+1]
                    savenumber = buycollect[i+2]
                    remainprice = int(sellprice) - int(saveprice)
                    #매도량과 종목이름 저장
                    p.stock_item_save(sellname, sellnumber)
                    #매도량이 매수량보다 많은지 확인
                    checkcode = p.stock_item_check(sellname, savenumber)
                else:
                    pass
                #정상
            if(checkcode == 1):
                #매도한 정보 저장
                p.sell_save(sellname, sellprice, sellnumber)
                #수익률 정보 저장
                p.profit_and_loss(sellname, saveprice, sellprice, remainprice, sellnumber)
                check ="1"
            #매도량이 매수량을 넘음
            else:
                #추가되어서 넘친 매도량 삭제
                p.stock_item_correct(sellname)
                check="2"
                print("알림 : <매도 수량을 다시입력해주세요>")
        else:
            return redirect("/")
        file.write(check)
        file.close()
    except:
        return redirect("/portfolio")
    return render_template("portfolioSell_return.html")

#종목 매도 완료
@app.route("/portfolio/sellreturn")
def portfolioSellReturn():
    try:
        try:
            if(session['ID']):
                pass
        except:
            flash("로그인을 먼저 해주세요.")
            return render_template("login.html")
        path="/nomadcoders/boot/DB/check.txt"
        file = open(path, 'r')
        Check=int(file.read())
        file.close()
        file2 = open(path, 'w')
        file2.close()
        print(Check)
        if(Check!=0):
            pass
        else:
            return redirect("/portfolio")
    except:
        return redirect("/portfolio")
    return render_template("portfolioSellReturn.html",checkcode = Check)

#포트폴리오 출력
@app.route("/portfolio/inquiry")
def portfolioInquiry():
    #초기 리스트 생성
    try:
        try:
            if(session['ID']):
                pass
        except:
            flash("로그인을 먼저 해주세요.")
            return render_template("login.html")
        global p
        Buyitem= []
        get_code = []
        get_profit = []
        get_presentrate = []
        get_presentprofit = []
        Buyremain=[]
        sell_already=[]
        ptotal=[]
        ltotal=[]
        last_total=0
        present_total=0
        longline = "\n"
        #매수 정보 불러옴
        Buyinfor = p.buy_open()
        Sellinfor = p.sell_open()
        Size = len(Buyinfor) / 3
        for i in range(0,int(Size)):
            #매수 종목을 리스트에 저장
            Buyitem.append(Buyinfor[3*i])
        for i in range(0,len(Buyitem)):
            for j in range(0,len(Buyinfor)):
                #종목 이름이 들어있는 항목의 위치를 찾음
                if(Buyitem[i] == Buyinfor[j]):
                    #매도한 내용이 있는지 확인
                    if(len(Sellinfor) != 0):
                        for s in range(0,len(Sellinfor)):
                            if(Buyinfor[j] == Sellinfor[s]):
                                if(Sellinfor[s] not in sell_already):
                                    #해당 종목의 매도량을 저장함
                                    stocknumber = p.stock_item_open(Buyitem[i])
                                    #현재 남은 수량을 저장함
                                    Buyremain = int(Buyinfor[j+2]) - stocknumber
                                    #리스트에 최신화(리스트를 이용하여 출력할 것이기 때문이다.)
                                    Buyinfor[j+2] = Buyremain
                                    sell_already.append(Sellinfor[s])
                                    #코드만 불러옴
                                else:
                                    pass
                            else:
                                Buyremain = Buyinfor[j+2]
                    else:
                        #매도 내용이 없으면 현재 수량을 남은 수량으로 저장
                        Buyremain = Buyinfor[j+2]
                    #최종적으로 종목을 출력 형식에 맞게 값을 변형시킴
                    df_krx = c.KRX_connect()
                    get_code = df_krx[df_krx.Name==Buyitem[i]].Symbol.values[0].strip()  
                    get_profit, get_presentrate, get_presentprofit,get_ptotal,get_ltotal = p.present_rate(get_code,Buyitem[i],Buyinfor[j+1],Buyremain) 
                    ptotal.append(get_ptotal)
                    ltotal.append(get_ltotal)
                    Buyinfor.insert(j+2,get_presentrate)
                    Buyinfor.insert(j+3,get_profit)
                    Buyinfor.insert(j+5,get_presentprofit)
                    Buyinfor.insert(j+6,longline)
                else:
                    pass
        for l in range(0, len(Buyinfor)):
            if(Buyinfor[l] == 0):
                #만약 남은 수량이 0이라면 해당 정보가 출력되지 않게 삭제함
                del Buyinfor[l-4:l+3]
                break
            else:
                pass

        #입력된 내용을 형식적으로 다듬는 과정
        for k in range(0,len(Buyinfor)):
            if(k%7 == 1 ):
                average_rate = Buyinfor[k]
                get_average = format(int(average_rate),',')
                average = "평단가 : "+ get_average+"원"
                Buyinfor[k] = average
            elif(k%7 == 4):
                amount = Buyinfor[k]
                get_amount = format(int(amount),',')
                stock_amount = "수량 : " + get_amount+"주"
                Buyinfor[k] = stock_amount
            else:
                pass
        #총합 값 계산
        for n in range(0,len(ltotal)):
            last_total += ltotal[n] 
            present_total += ptotal[n] 
        #형식에 맞게 값 저장
        get_latotal = format(last_total,',')
        get_prtotal = format(present_total,',')
        if(present_total-last_total== 0):
            Buyinfor.append("구매 총합 : "+get_latotal+"원")
            Buyinfor.append("현재 총합 : "+get_prtotal+"원")
        else:
            total_profit = (present_total-last_total)/last_total*100
            Buyinfor.append("구매 총합 : "+get_latotal+"원")
            Buyinfor.append("현재 총합 : "+get_prtotal+"원")
            Buyinfor.append("총 수익률 : "+"{:0,.2f}".format(total_profit)+"%")
        portfolio_len =len(Buyinfor)
        return render_template("portfolioInquiry.html",portfolio=Buyinfor,portfolio_len=portfolio_len)
    except:
        return render_template("portfolio.html")

#매도 수익 출력
@app.route("/portfolio/return")
def portfolioReturn():
    try:
        if(session['ID']):
            pass
        PLcollect = p.pl_open()
        if PLcollect:
            length = len(PLcollect)
        else:
            return redirect("/")
        return render_template("/portfolioReturn.html",PLcollect=PLcollect,len=length)
    except:
            flash("로그인을 먼저 해주세요.")
            return render_template("login.html")


#포트폴리오 초기화 여부 확인
@app.route("/portfolio/init")
def portfolioInit():
    try:
        if(session['ID']):
            return render_template("/portfolioInit.html")
    except:
        flash("로그인을 먼저 해주세요.")
        return render_template("login.html")

#포트폴리오 초기화
@app.route("/portfolio/init_return")
def portfolioInit_return():
    try:
        if(session['ID']):
            pass
        initialize = request.args.get('initialize')
        if(initialize=="초기화"):
            stock_item = p.buy_open()
            p.portfolio_initialize(stock_item)
        else:
            pass
        return render_template("/portfolioInit_return.html",initialize=initialize)
    except:
            flash("로그인을 먼저 해주세요.")
            return render_template("login.html")


app.run(host="0.0.0.0", debug=True)