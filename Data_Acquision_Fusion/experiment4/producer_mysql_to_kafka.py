import json
import pymysql
from kafka import KafkaProducer

# 连接MySQL数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='testDB'
)
cursor = conn.cursor()

# 查询student表数据
query = "SELECT * FROM student"
cursor.execute(query)
rows = cursor.fetchall()

# 将数据转换为JSON格式
data = []
for row in rows:
    student = {
        "sno": row[0],
        "sname": row[1],
        "ssex": row[2],
        "sage": row[3]
    }
    data.append(student)
json_data = json.dumps(data)

# 发送数据到Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('student_topic', json_data.encode('utf-8'))
producer.close()

# 关闭数据库连接
cursor.close()
conn.close()