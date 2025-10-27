from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['supermarket']

# 求各商品销售量，并按销售量大小排序
pipeline = [
    {
        "$group": {
            "_id": "$good_name",
            "total_amount": {"$sum": "$amount"}
        }
    },
    {
        "$sort": {"total_amount": -1}
    }
]

result = list(collection.aggregate(pipeline))
print(result)

# 关闭连接
client.close()