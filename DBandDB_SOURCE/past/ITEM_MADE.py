import pandas as pd
import pickle

#pandas 모듈을 사용하여 html을 읽어와 데이터프레임을 생성한다.
stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0] 
# 필요한 것은 "회사명"과 "종목코드" 이므로 필요없는 column들은 제외
stock_code = stock_code[['회사명']] 
company = []
company = stock_code['회사명'].values

with open('ITEM.txt','w',encoding='UTF-8') as f:
    for name in company:
        f.write('\"{name}\",\n'.format(name=company))