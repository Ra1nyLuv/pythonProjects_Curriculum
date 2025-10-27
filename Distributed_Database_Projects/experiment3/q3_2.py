from pymongo import MongoClient

# 连接MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 创建或选择数据库
db = client['mytest']

# 创建或选择集合
collection = db['laptop']

# 插入单个文档
doc_to_insert = {"_id": 200, "brand": "Huawei", "CPU": "intel i7", "price": 6900, "amount": 82}
if collection.count_documents({"_id": 200}) == 0:
    result = collection.insert_one(doc_to_insert)
    print(f"Inserted ID: {result.inserted_id}")
else:
    print("Document with _id 200 already exists!")

# 插入多个文档
docs_to_insert = [
    {"_id": 103, "brand": "Dell", "CPU": "intel i3", "price": 3500, "amount": 35},
    {"_id": 93, "brand": "Lenovo", "CPU": "intel i7", "price": 6200, "amount": 55}
]
if collection.count_documents({"_id": {"$in": [103, 93]}}) == 0:
    result = collection.insert_many(docs_to_insert)
    print(f"Inserted IDs: {result.inserted_ids}")
else:
    print("Documents with _id 103 or 93 already exist!")

# 关闭连接
client.close()