import FinanceDataReader as fdr
import pickle

df_nasdaq = fdr.StockListing('NASDAQ')
df_nasdaq = df_nasdaq[['Name','Symbol']]
codepath="./nasdaq.txt"
f = open(codepath,"w")
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 
df_nasdaq.to_pickle(codepath)
f.close()

