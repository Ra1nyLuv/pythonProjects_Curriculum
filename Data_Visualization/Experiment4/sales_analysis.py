import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建数据
data = {
    '年度': [2019, 2019, 2019, 2019, 2019, 2019, 2020, 2020, 2020, 2020, 2020, 2020],
    '地区': ['中南', '东北', '华东', '华北', '西南', '西北'] * 2,
    '销售额': [214.71, 445.66, 627.11, 800.73, 956.88, 1090.24,
            223.65, 488.28, 673.34, 870.95, 1027.34, 1193.34]
}
df = pd.DataFrame(data)

# 复式条状图
plt.figure(figsize=(12, 6))
sns.barplot(x='地区', y='销售额', hue='年度', data=df, palette='Set2')
plt.title('某企业两个年度销售额情况（条状图）')
plt.xlabel('地区')
plt.ylabel('销售额（单位：万元）')
plt.legend(title='年度')
plt.savefig('sales_bar.png')
plt.show()

# 折线图
plt.figure(figsize=(12, 6))
sns.lineplot(x='地区', y='销售额', hue='年度', data=df, marker='o', markersize=8)
plt.title('某企业两个年度销售额情况（折线图）')
plt.xlabel('地区')
plt.ylabel('销售额（单位：万元）')
plt.grid(True)
plt.savefig('sales_line.png')
plt.show()