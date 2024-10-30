from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['supermarket']

# 求每年每月每日促销订单数量和销售金额
pipeline = [
    {
        "$match": {
            "is_promote": "是"
        }
    },
    {
        "$group": {
            "_id": {
                "year": {"$year": "$sale_date"},
                "month": {"$month": "$sale_date"},
                "day": {"$dayOfMonth": "$sale_date"}
            },
            "order_count": {"$sum": 1},
            "total_sales": {"$sum": {"$multiply": ["$amount", "$price"]}}
        }
    },
    {
        "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}
    }
]

result = list(collection.aggregate(pipeline))
print(result)

# 关闭连接
client.close()