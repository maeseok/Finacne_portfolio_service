import pymongo


def db_connect(dbname):
    client = pymongo.MongoClient("mongodb+srv://maeseok:didc001@finance.smjhg.mongodb.net/members?retryWrites=true&w=majority")
    db = client.dbname
    return db
# # 저장 - 예시


def KRW_made(symbol,stock_rate,db):
    DOC = {'Symbol':symbol,'Name':stock_rate[1],'Rate':stock_rate[2],'Gap':stock_rate[3],'Profit':stock_rate[4]}
    db.users.insert_one(DOC)

def KRW_inquiry():
    items = db.users.find()
    return items


    #doc = {'name':'bobby','age':21}
#db.users.insert_one(doc)
#
# # 한 개 찾기 - 예시
#user = db.users.find_one({'name':'bobby'})
#
# # 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
#same_ages = list(db.users.find({'age':21},{'_id':False}))
#
# # 바꾸기 - 예시
#db.users.update_one({'name':'bobby'},{'$set':{'age':19}})
#
# # 지우기 - 예시
#db.users.delete_one({'name':'bobby'})