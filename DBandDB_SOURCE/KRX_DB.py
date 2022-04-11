import FinanceDataReader as fdr
import pickle
import pymongo
client = pymongo.MongoClient("mongodb+srv://maeseok:didc001@finance.smjhg.mongodb.net/data?retryWrites=true&w=majority")
KRX = client['KRX']
df_amex = fdr.StockListing('KRX')
df_amex = df_amex[['Name','Symbol']]
df_dict = df_amex.to_dict("records")
print(df_dict)
KRX.data2.insert_many(df_dict)

#각각 형태로 7600개 저장하기로 함!