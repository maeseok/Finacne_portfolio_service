import FinanceDataReader as fdr
import pickle

df_nyse = fdr.StockListing('NYSE')
df_nyse = df_nyse[['Name']]
company = []
company = df_nyse['Name'].values
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 

with open('nyseITEM.txt','w',encoding='UTF-8') as f:
    for name in company:
        f.write('\"{name}\",\n'.format(name=name))
