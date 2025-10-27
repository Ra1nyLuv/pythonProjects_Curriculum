from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['supermarket']

# 求1月份日购买数量排名前五的购买数量和日期
pipeline = [
    {
        "$match": {
            "sale_month": 201501
        }
    },
    {
        "$group": {
            "_id": {
                "date": "$sale_date"
            },
            "total_amount": {"$sum": "$amount"}
        }
    },
    {
        "$sort": {"total_amount": -1}
    },
    {
        "$limit": 5
    }
]

result = list(collection.aggregate(pipeline))
print(result)

# 关闭连接
client.close()