import FinanceDataReader as fdr
import pickle
import pymongo
client = pymongo.MongoClient("mongodb+srv://maeseok:didc001@finance.smjhg.mongodb.net/etfus?retryWrites=true&w=majority")
ETFUS = client['ETFUS']

df_etfus = fdr.StockListing('ETF/US')
df_etfus = df_etfus[['Name','Symbol']]
df_dict = df_etfus.to_dict("records")
print(df_dict)
ETFUS.data.insert_many(df_dict)

