import FinanceDataReader as fdr
import pickle

df_amex = fdr.StockListing('AMEX')
df_amex = df_amex[['Name']]
company = []
company = df_amex['Name'].values
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 

with open('amexITEM.txt','w',encoding='UTF-8') as f:
    for name in company:
        f.write('\"{name}\",\n'.format(name=name))
