import pymysql

db = pymysql.connect(host = "localhost", user = 'root', password = 'cjl1013jj', database = 'studentsdb', charset='utf8')

cursor = db.cursor()

stno = ['0002']

try:
    cursor.callproc('grade_pro', args = stno)
    db.commit()
    tb = cursor.fetchall()
    for row in tb:
        print(row)
except:
    cursor.fetchall()

cursor.close()
db.close()
