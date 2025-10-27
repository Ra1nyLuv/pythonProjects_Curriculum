from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['laptop']

# 计算库存总金额和数量
pipeline = [
    {'$group': {'_id': None, 'total_amount': {'$sum': '$amount'}, 'total_value': {'$sum': {'$multiply': ['$price', '$amount']}}}}
]
docs = collection.aggregate(pipeline)
for doc in docs:
    print(doc)

# 计算各品牌笔记本电脑价格的平均值
pipeline = [
    {'$group': {'_id': '$brand', 'average_price': {'$avg': '$price'}}},
    {'$project': {'_id': 1, 'average_price': {'$round': ['$average_price', 2]}}}
]
docs = collection.aggregate(pipeline)
for doc in docs:
    print(doc)

# 按CPU分组计算数量之和
pipeline = [
    {'$group': {'_id': '$CPU', 'total_amount': {'$sum': '$amount'}}}
]
docs = collection.aggregate(pipeline)
for doc in docs:
    print(doc)

# 按数量从小到大排序的品牌电脑库存
pipeline = [
    {'$group': {'_id': '$brand', 'total_amount': {'$sum': '$amount'}}},
    {'$sort': {'total_amount': 1}},
    {'$limit': 1}
]
docs = collection.aggregate(pipeline)
for doc in docs:
    print(doc)

# 关闭连接
client.close()