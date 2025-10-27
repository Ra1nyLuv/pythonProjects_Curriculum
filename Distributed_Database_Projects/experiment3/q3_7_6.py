from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['supermarket']

# 求各大类每个二级分类销售金额和销售数量，要求销售金额按保留两位小数显示
pipeline = [
    {
        "$group": {
            "_id": {
                "big_name": "$big_name",
                "m_name": "$m_name"
            },
            "total_sales": {"$sum": {"$multiply": ["$amount", "$price"]}},
            "total_amount": {"$sum": "$amount"}
        }
    },
    {
        "$addFields": {
            "total_sales": {"$round": ["$total_sales", 2]}
        }
    },
    {
        "$sort": {"_id.big_name": 1, "_id.m_name": 1}
    }
]

result = list(collection.aggregate(pipeline))
print(result)

# 关闭连接
client.close()