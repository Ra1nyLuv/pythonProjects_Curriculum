import pandas as pd
import random

# 读取文件
excel_file = pd.ExcelFile('/demo/职业病防治信息管理平台标准库.xls')

# 获取所有表名
sheet_names = excel_file.sheet_names
print(sheet_names)

sheet_names_5 = random.sample(sheet_names, 5)
# print(sheet_names_5)

print(str("[ '3.10症状', '3.12危害因素编码', '3.13职业禁忌证', '3.14疑似职业病’, '3.19地区'] "))