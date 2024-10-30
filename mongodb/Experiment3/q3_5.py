from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['laptop']

# 查找特定条件的文档
docs = collection.find({'$or': [{'price': {'$lt': 5000, '$gt': 4000}}, {'amount': 100}]})
for doc in docs:
    print(doc)

# 关闭连接
client.close()