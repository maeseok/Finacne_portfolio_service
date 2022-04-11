import FinanceDataReader as fdr
import pickle
import pymongo
client = pymongo.MongoClient("mongodb+srv://maeseok:didc001@finance.smjhg.mongodb.net/nasdaq?retryWrites=true&w=majority")
NASDAQ = client['NASDAQ']
df_nasdaq = fdr.StockListing('NASDAQ')
df_nasdaq = df_nasdaq[['Name','Symbol']]

df_dict = df_nasdaq.to_dict("records")
print(df_dict)
NASDAQ.data.insert_many(df_dict)


