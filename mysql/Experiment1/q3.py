import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='SchoolDB'
)
cursor = conn.cursor()

# 更新语句
query = """UPDATE Course SET Credit = 5 WHERE Cno = 00001 AND Cname = 'Database';
            
"""
# 执行更新
cursor.execute(query)
cursor.execute("SELECT * FROM Course;")
conn.commit()

# 关闭连接
cursor.close()
conn.close()