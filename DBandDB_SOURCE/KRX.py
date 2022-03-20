import FinanceDataReader as fdr
import pickle

df_amex = fdr.StockListing('KRX')
df_amex = df_amex[['Name','Symbol']]
codepath="./code2.txt"
f = open(codepath,"w")
#pickle 모듈을 사용하여 dataframe 타입을 파일에 저장한다. 
df_amex.to_pickle(codepath)
f.close()