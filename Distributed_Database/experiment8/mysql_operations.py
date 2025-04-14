import pymysql

db = pymysql.connect(host="localhost", user="root", password="1234", database="coursesel", charset="utf8")
try:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM studentinfo")
    stuInfo = cursor.fetchall()
    for row in stuInfo:
        id = row[0]
        name = row[1]
        age = row[2]
        sex = row[3]

        print("学生信息：" + str(id) + "," + str(name) + "," + str(age) + "," + str(sex))

        # 使用参数化查询，避免SQL注入风险
        sqlCourse = "SELECT courseinfo.courseName, gradeinfo.score " \
                    "FROM studentinfo, courseinfo, gradeinfo " \
                    "WHERE studentinfo.studentNo=gradeinfo.studentNo " \
                    "and courseinfo.courseNo=gradeinfo.courseNo and studentinfo.studentNo=%s"
        cursor1 = db.cursor()
        try:
            cursor1.execute(sqlCourse, (id,))
            courses = cursor1.fetchall()
            for course in courses:
                course_name = course[0]
                score = course[1]
                print(f"课程名：{course_name}，成绩：{score}")
        except:
            print("查询课程信息时出现错误")
        finally:
            cursor1.close()  # 确保游标能正确关闭

finally:
    cursor.close()
    db.close()