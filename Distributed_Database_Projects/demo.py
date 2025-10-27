from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 选择数据库
db = client['mytest']

# 选择集合
collection = db['laptop']

# 删除集合中的所有文档
result = collection.delete_many({})

# 输出删除结果
print(f"Deleted {result.deleted_count} documents from the 'laptop' collection.")

# 关闭连接
client.close()