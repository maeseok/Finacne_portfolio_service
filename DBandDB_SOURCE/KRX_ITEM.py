import FinanceDataReader as fdr
import pickle

df_krx = fdr.StockListing('KRX')
df_krx = df_krx[['Name']]
company = []
company = df_krx['Name'].values
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 

with open('krxITEM.txt','w',encoding='UTF-8') as f:
    for name in company:
        f.write('\"{name}\",\n'.format(name=name))
