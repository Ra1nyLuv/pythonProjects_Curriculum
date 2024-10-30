from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['laptop']

# 删除单个文档
result = collection.delete_one({'_id': 200})
print(f"Deleted count: {result.deleted_count}")

# 关闭连接
client.close()