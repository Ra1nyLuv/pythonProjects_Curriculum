# 创建堆叠面积图
plt.figure(figsize=(12, 6))
plt.stackplot(df['年份'], 
             df['0-14岁人口(万人)'], 
             df['15-64岁人口(万人)'],
             df['65岁及以上人口(万人)'],
             labels=['0-14岁', '15-64岁', '65岁+'])

plt.title('中国人口年龄结构比例变化')
plt.xlabel('年份')
plt.ylabel('人口（万人）')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()