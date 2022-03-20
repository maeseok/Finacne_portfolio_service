import FinanceDataReader as fdr
import pickle

df_nasdaq = fdr.StockListing('NASDAQ')
df_nasdaq = df_nasdaq[['Name']]
company = []
company = df_nasdaq['Name'].values
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 

with open('nasdaqITEM.txt','w',encoding='UTF-8') as f:
    for name in company:
        f.write('\"{name}\",\n'.format(name=name))
