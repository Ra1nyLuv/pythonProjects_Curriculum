import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager  # 导入字体管理模块

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

# 读取数据
data = {
    '年份': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008],
    '就业人员（万人）': [72085, 72797, 73280, 73736, 74264, 74647, 74978, 75321, 75564],
    '第一产业就业人员（万人）': [36042.5, 36398.5, 36640, 36204.4, 34829.8, 33441.9, 31940.6, 30731, 29923.3],
    '第二产业就业人员（万人）': [16219.1, 16233.7, 15681.9, 15927, 16709.4, 17766, 18894.5, 20186, 20553.4],
    '第三产业就业人员（万人）': [19823.4, 20164.8, 20958.1, 21604.6, 22724.8, 23439.2, 24142.9, 24404, 25087.2]
}
df = pd.DataFrame(data)

# 散点图
plt.figure(figsize=(12, 6))
for column in df.columns[2:]:
    plt.scatter(df['年份'], df[column], label=column)
plt.title('2000-2019年各产业就业人员散点图')  # 中文标题
plt.xlabel('年份')
plt.ylabel('就业人员数量（万人）')
plt.legend()
plt.show()

# 折线图
plt.figure(figsize=(12, 6))
for column in df.columns[2:]:
    plt.plot(df['年份'], df[column], label=column, marker='o')
plt.title('2000-2019年各产业就业人员折线图')  # 中文标题
plt.xlabel('年份')
plt.ylabel('就业人员数量（万人）')
plt.legend()
plt.show()

# 饼图（2019年）
last_year_data = df.iloc[-1][2:]
plt.figure(figsize=(8, 8))
plt.pie(last_year_data, labels=last_year_data.index, autopct='%1.1f%%', startangle=90)
plt.title('2019年各产业就业人员饼图')  # 中文标题
plt.show()

# 分组柱形图
x = df['年份']
bar_width = 0.2
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - bar_width, df['第一产业就业人员（万人）'], width=bar_width, label='第一产业')
ax.bar(x, df['第二产业就业人员（万人）'], width=bar_width, label='第二产业')
ax.bar(x + bar_width, df['第三产业就业人员（万人）'], width=bar_width, label='第三产业')
ax.set_title('2000-2019年各产业就业人员分组柱形图')  # 中文标题
ax.set_xlabel('年份')
ax.set_ylabel('就业人员数量（万人）')
ax.legend()
plt.show()

# 堆叠柱形图
plt.figure(figsize=(12, 6))
plt.bar(x, df['第一产业就业人员（万人）'], label='第一产业')
plt.bar(x, df['第二产业就业人员（万人）'], bottom=df['第一产业就业人员（万人）'], label='第二产业')
plt.bar(x, df['第三产业就业人员（万人）'], bottom=df['第一产业就业人员（万人）'] + df['第二产业就业人员（万人）'], label='第三产业')
plt.title('2000-2019年各产业就业人员堆叠柱形图')  # 中文标题
plt.xlabel('年份')
plt.ylabel('就业人员数量（万人）')
plt.legend()
plt.show()

# 箱线图
plt.figure(figsize=(10, 6))
box_data = [df['第一产业就业人员（万人）'], df['第二产业就业人员（万人）'], df['第三产业就业人员（万人）']]
plt.boxplot(box_data, labels=['第一产业', '第二产业', '第三产业'])
plt.title('2000-2019年各产业就业人员箱线图')  # 中文标题
plt.ylabel('就业人员数量（万人）')
plt.show()