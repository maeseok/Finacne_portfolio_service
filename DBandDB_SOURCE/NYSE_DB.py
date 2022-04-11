import FinanceDataReader as fdr
import pickle
import pymongo
client = pymongo.MongoClient("mongodb+srv://maeseok:didc001@finance.smjhg.mongodb.net/nyse?retryWrites=true&w=majority")
NYSE = client['NYSE']
df_nyse = fdr.StockListing('NYSE')
df_nyse = df_nyse[['Name','Symbol']]

df_dict = df_nyse.to_dict("records")
print(df_dict)
NYSE.data.insert_many(df_dict)

