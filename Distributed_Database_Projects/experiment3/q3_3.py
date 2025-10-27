from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['laptop']

# 更新单个文档
condition = {'brand': 'Dell', 'CPU': 'intel i5'}
new_price = 5000
result = collection.update_one(condition, {'$set': {'price': new_price}})
print(f"Modified count: {result.modified_count}")

# 更新多个文档
condition = {'price': {'$lte': 4000}}
increase_amount = 50
result = collection.update_many(condition, {'$inc': {'price': increase_amount}})
print(f"Matched count: {result.matched_count}, Modified count: {result.modified_count}")

# 关闭连接
client.close()