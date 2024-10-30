import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='SchoolDB'
)
cursor = conn.cursor()

# 插入语句
query = "INSERT INTO SC (Sno, Cno, Grade) VALUES (10005, 00004, 73)"

# 执行插入
cursor.execute(query)

conn.commit()

# 关闭连接
cursor.close()
conn.close()