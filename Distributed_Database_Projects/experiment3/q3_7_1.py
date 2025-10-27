from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['supermarket']

# 求最大销售金额的中类名称和最大销售金额
pipeline = [
    {
        "$group": {
            "_id": "$m_name",
            "max_sales": {"$max": {"$multiply": ["$amount", "$price"]}}
        }
    },
    {
        "$sort": {"max_sales": -1}
    },
    {
        "$limit": 1
    }
]

result = list(collection.aggregate(pipeline))
print(result)

# 关闭连接
client.close()