import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='SchoolDB'
)
cursor = conn.cursor()

# 删除SC表中的记录
query1 = "DELETE FROM SC WHERE Sno = 10003"
cursor.execute(query1)
conn.commit()

# 删除Student表中的记录
query2 = "DELETE FROM Student WHERE Sno = 10003"
cursor.execute(query2)
conn.commit()

# 关闭连接
cursor.close()
conn.close()