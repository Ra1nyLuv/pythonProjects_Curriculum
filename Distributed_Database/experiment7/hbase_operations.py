import happybase

# 连接到HBase
conn = happybase.Connection('192.168.221.101', 9090)

# 创建表
tablename = 'ptu_student'
existing_tables = [t.decode() for t in conn.tables()]
if tablename not in existing_tables:
    families = {
        "studentinfo": dict(),
        "courseinfo": dict()
    }
    conn.create_table(tablename, families)
    print("-----------------")
    print("创建表操作：成功创建表 ptu_student。")
else:
    print("-----------------")
    print("创建表操作：表 ptu_student 已存在。")

# 获取表对象
table = conn.table(tablename)

# 添加数据
data = [
    ("s_id0001", {"studentinfo:name": "student1", "studentinfo:age": "20", "studentinfo:sex": "female", "studentinfo:class": "data01", "courseinfo:Hadoop": "89", "courseinfo:DataBase": "90", "courseinfo:Python": "88"}),
    ("s_id0002", {"studentinfo:name": "student2", "studentinfo:age": "21", "studentinfo:sex": "male", "studentinfo:class": "data03", "courseinfo:Hadoop": "79", "courseinfo:DataBase": "80", "courseinfo:Python": "85"}),
    ("s_id0003", {"studentinfo:name": "student3", "studentinfo:sex": "male", "studentinfo:class": "data05", "courseinfo:Hadoop": "90", "courseinfo:DataBase": "91", "courseinfo:Python": "92"}),
    ("s_id0004", {"studentinfo:name": "student4", "studentinfo:age": "19", "studentinfo:class": "data02", "courseinfo:Hadoop": "68", "courseinfo:DataBase": "78", "courseinfo:Python": "88"}),
    ("s_id0005", {"studentinfo:name": "student5", "studentinfo:age": "20", "studentinfo:sex": "femal", "studentinfo:class": "data02", "courseinfo:Hadoop": "87", "courseinfo:DataBase": "90", "courseinfo:Python": "78"})
]
for row_key, row_data in data:
    table.put(row_key, row_data)
print("-----------------")
print("添加数据操作：成功向 ptu_student 表插入数据。")

# 查询所有数据并打印
print("-----------------")
print("查询所有数据操作：")
for key, dict_value in table.scan():
    key = key.decode()
    print(key)
    for dict_key, d_value in dict_value.items():
        dict_key = dict_key.decode()
        d_value = d_value.decode()
        print(dict_key, ":", d_value)

# 删除指定数据
table.delete("s_id0005", ["studentinfo:age"])
print("-----------------")
print("删除数据操作：成功删除行键为's_id0005'，列族'studentinfo'，列'age'的数据。")

# 查询行键为's_id0004'的数据并打印
print("-----------------")
print("查询行键's_id0004'数据操作：")
one_row = table.row('s_id0004')
for value in one_row.keys():
    print(value.decode('utf-8'), one_row[value].decode('utf-8'))

# 行键过滤器查询
scan_filter = "RowFilter(=, 'binary:s_id0004')"
result = table.scan(filter=scan_filter)
print("-----------------")
print("行键过滤器查询操作（获取行键's_id0004'的数据）：")
for key, dict_value in result:
    key = key.decode()
    print(key)
    for dict_key, d_value in dict_value.items():
        dict_key = dict_key.decode()
        d_value = d_value.decode()
        print(dict_key, ":", d_value)

# 值过滤器查询
scan_filter = "ValueFilter(>,'binary:85')"
result = table.scan(filter=scan_filter)
print("-----------------")
print("值过滤器查询操作（获取值大于85的数据）：")
for key, dict_value in result:
    key = key.decode()
    print(key)
    for dict_key, d_value in dict_value.items():
        dict_key = dict_key.decode()
        d_value = d_value.decode()
        print(dict_key, ":", d_value)

# PrefixFilter查询
scan_filter = "PrefixFilter('s_id')"
result = table.scan(filter=scan_filter)
print("-----------------")
print("PrefixFilter查询操作（获取以's_id'开头的学号对应的数据）：")
for key, dict_value in result:
    key = key.decode()
    print(key)
    for dict_key, d_value in dict_value.items():
        dict_key = dict_key.decode()
        d_value = d_value.decode()
        print(dict_key, ":", d_value)

# FamilyFilter查询
scan_filter = "FamilyFilter(=,'substring:studentinfo')"
result = table.scan(filter=scan_filter)
print("-----------------")
print("FamilyFilter查询操作（获取只包含列族'studentinfo'的数据）：")
for key, dict_value in result:
    key = key.decode()
    print(key)
    for dict_key, d_value in dict_value.items():
        dict_key = dict_key.decode()
        d_value = d_value.decode()
        print(dict_key, ":", d_value)

# QualifierFilter查询
scan_filter = "QualifierFilter(=, 'substring:Python')"
result = table.scan(filter=scan_filter)
print("-----------------")
print("QualifierFilter查询操作（获取列名包含'Python'的数据）：")
for key, dict_value in result:
    key = key.decode()
    print(key)
    for dict_key, d_value in dict_value.items():
        dict_key = dict_key.decode()
        d_value = d_value.decode()
        print(dict_key, ":", d_value)

# RowFilter和SingleColumnValueFilter组合查询
scan_filter = "RowFilter(=, 'binary:s_id0') AND SingleColumnValueFilter('studentinfo','sex', =, 'binary:female')"
result = table.scan(filter=scan_filter)
print("-----------------")
print("组合过滤器查询操作（获取学号以's_id0'开头且性别为'female'的数据）：")
for key, dict_value in result:
    key = key.decode()
    print(key)
    for dict_key, d_value in dict_value.items():
        dict_key = dict_key.decode()
        d_value = d_value.decode()
        print(dict_key, ":", d_value)

# 关闭连接
conn.close()