import csv

with open('grades.csv', mode='r') as file:
    reader = csv.reader(file)
    rows = [row for row in reader]
    header = rows[0]
    header.append('总评成绩')
    for row in rows[1:]:
        平时成绩 = int(row[2])
        期末成绩 = int(row[3])
        总评成绩 = int(平时成绩 * 0.3 + 期末成绩 * 0.7)
        row.append(str(总评成绩))
with open('grades_with_total.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
