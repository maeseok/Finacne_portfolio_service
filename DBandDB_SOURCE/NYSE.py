import FinanceDataReader as fdr
import pickle

df_nyse = fdr.StockListing('NYSE')
df_nyse = df_nasdaq[['Name','Symbol']]
codepath="./nyse.txt"
f = open(codepath,"w")
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 
df_nyse.to_pickle(codepath)
f.close()

