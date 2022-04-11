import FinanceDataReader as fdr
import pickle
import pymongo
client = pymongo.MongoClient("mongodb+srv://maeseok:didc001@finance.smjhg.mongodb.net/amex?retryWrites=true&w=majority")
AMEX = client['AMEX']

df_amex = fdr.StockListing('AMEX')
df_amex = df_amex[['Name','Symbol']]
df_dict = df_amex.to_dict("records")
AMEX.data.insert_many(df_dict)

