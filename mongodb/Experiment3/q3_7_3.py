from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['supermarket']

# 求2015年1月份订单数量
pipeline_sum = [
    {
        "$match": {
            "sale_month": 201501
        }
    },
    {
        "$group": {
            "_id": None,
            "order_count": {"$sum": 1}
        }
    }
]

pipeline_count = [
    {
        "$match": {
            "sale_month": 201501
        }
    }
]

result_sum = list(collection.aggregate(pipeline_sum))
result_count = collection.count_documents({"sale_month": 201501})

print(f"Using $sum: {result_sum[0]['order_count']}")
print(f"Using count(): {result_count}")

# 关闭连接
client.close()