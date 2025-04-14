import happybase

# 连接HBase数据库
print("正在连接HBase数据库...")
conn = happybase.Connection('localhost', 9090)
print("HBase数据库连接成功！")

# 检查表是否存在
existing_tables = conn.tables()
if b'courseGrade' in existing_tables:
    print("表 'courseGrade' 已存在。")
else:
    print("表 'courseGrade' 不存在，准备创建该表。")
    tablename = 'courseGrade'
    families = {
        "StuInfo": dict(),
        "Grades": dict()
    }
    conn.create_table(tablename, families)
    print("表 'courseGrade' 创建成功！")

try:
    # 此处直接删掉获取游标这行代码，不需要游标操作
    # cursor = conn.cursor()
    # 假设已经有合适的方式获取到studentinfo表的数据，这里简化为直接定义一个示例数据结构
    stuInfo = [(1, '张三', 20, '男'), (2, '李四', 21, '女')]
    print("成功获取学生信息，记录数量:", len(stuInfo))

    table = conn.table('courseGrade')
    for row in stuInfo:
        id = row[0]
        name = row[1]
        age = row[2]
        sex = row[3]

        # 向列族StuInfo插入数据
        table.put(str(id), {'StuInfo:name': str(name), 'StuInfo:age': str(age), 'StuInfo:sex': str(sex)})
        print(f"已将学号为 {id} 的学生基本信息插入 'courseGrade' 表的StuInfo列族")

        # 根据学号id查询该学生所选课程相关信息（此处SQL语句需根据实际优化，目前仅示例逻辑）
        sqlCourse = "SELECT courseinfo.courseName,gradeinfo.score " \
                    "FROM studentinfo,courseinfo,Gradeinfo " \
                    "WHERE studentinfo.studentNo=Gradeinfo.studentNo " \
                    "and courseinfo.courseNo=Gradeinfo.courseNo and studentinfo.studentNo='%s'" % (str(id))
        courses = []  # 假设此处获取到课程数据，实际需完善查询逻辑
        for course in courses:
            courseName = course[0]
            score = course[1]
            table.put(str(id), {"Grades:" + courseName: str(score)})
            print(f"已将学号为 {id} 的学生课程 {courseName} 及成绩 {score} 信息插入 'courseGrade' 表的Grades列族")

    # 用scan列出所有键值对
    print("开始扫描 'courseGrade' 表获取所有键值对:")
    for key, dict_value in table.scan():
        key = key.decode('utf-8')
        print("行键:", key)
        for dict_key, d_value in dict_value.items():
            dict_key = dict_key.decode('utf-8')
            d_value = d_value.decode('utf-8')
            print(dict_key, ":", d_value)

    # 根据学号查询courseGrades表数据，使用行键过滤器RowFilter获取行键为1的键值对
    print("使用行键过滤器查询学号（行键）为1的学生信息:")
    scan_filter = "RowFilter(=, 'binary:1')"
    result = table.scan(filter=scan_filter)
    for row_key, row_data in result:
        row_key = row_key.decode('utf-8')
        print("行键:", row_key)
        for col_key, col_value in row_data.items():
            col_key = col_key.decode('utf-8')
            col_value = col_value.decode('utf-8')
            print(col_key, ":", col_value)

finally:
    # 关闭连接
    conn.close()
    print("已关闭HBase数据库连接")