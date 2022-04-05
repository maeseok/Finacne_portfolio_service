import FinanceDataReader as fdr
import pickle

df_etfus = fdr.StockListing('ETF/US')
df_etfus = df_etfus[['Name']]
company = []
company = df_etfus['Name'].values
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 

with open('etfusITEM.txt','w',encoding='UTF-8') as f:
    for name in company:
        f.write('\"{name}\",\n'.format(name=name))
