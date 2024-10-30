from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['laptop']

# 检查是否已有数据
if collection.count_documents({}) == 0:
    # 插入多条文档
    docs = [
        {'_id': 70, 'brand': 'ThinkBook', 'CPU': 'intel i7', 'price': 6000, 'amount': 30},
        {'_id': 80, 'brand': 'Huawei', 'CPU': 'intel i3', 'price': 3200, 'amount': 100},
        {'_id': 90, 'brand': 'Lenovo', 'CPU': 'intel i3', 'price': 3050, 'amount': 100},
        {'_id': 100, 'brand': 'Dell', 'CPU': 'intel i5', 'price': 4500, 'amount': 58},
        {'_id': 110, 'brand': 'acer', 'CPU': 'intel i5', 'price': 3400, 'amount': 50},
        {'_id': 120, 'brand': 'Hp', 'CPU': 'intel i7', 'price': 6800, 'amount': 76},
        {'_id': 126, 'brand': 'Hp', 'CPU': 'intel i5', 'price': 6000, 'amount': 65},
        {'_id': 105, 'brand': 'Dell', 'CPU': 'intel i7', 'price': 6300, 'amount': 48},
        {'_id': 83, 'brand': 'Huawei', 'CPU': 'intel i5', 'price': 4320, 'amount': 80}
    ]
    result = collection.insert_many(docs)
    print(f"Inserted IDs: {result.inserted_ids}")
else:
    print("Documents already exist!")

# 关闭连接
client.close()