import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='SchoolDB'
)
cursor = conn.cursor()

# 查询语句
query = """
SELECT s.Sno, s.Sname, s.Sdept, c.Cno, c.Cname, sc.Grade
FROM Student s
JOIN SC sc ON s.Sno = sc.Sno
JOIN Course c ON sc.Cno = c.Cno
WHERE sc.Grade > 85
"""

# 执行查询
cursor.execute(query)
results = cursor.fetchall()

# 输出结果
for row in results:
    print(row)

# 关闭连接
cursor.close()
conn.close()