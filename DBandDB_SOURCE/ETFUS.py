import FinanceDataReader as fdr
import pickle

df_etfus = fdr.StockListing('ETF/US')
df_etfus = df_etfus[['Name','Symbol']]
codepath="./etfus.txt"
f = open(codepath,"w")
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 
df_etfus.to_pickle(codepath)
f.close()

