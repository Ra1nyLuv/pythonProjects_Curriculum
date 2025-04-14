import pandas as pd
import random

# 读取文件
excel_file = pd.ExcelFile('/demo/职业病防治信息管理平台标准库.xls')

# 获取所有表名
sheet_names = excel_file.sheet_names
print(sheet_names)

sheet_names_5 = random.sample(sheet_names, 5)
print(sheet_names_5)
