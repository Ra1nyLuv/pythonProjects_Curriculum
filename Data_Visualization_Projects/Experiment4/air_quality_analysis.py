import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
try:
    aqi = pd.read_csv(r"Experiment4\aqi.csv", encoding='gbk')
except:
    aqi = pd.read_csv(r"Experiment4\aqi.csv", encoding='utf-8')

# 任务三实训1
# 散点图
plt.figure(figsize=(12, 8))
sns.scatterplot(x='PM2.5含量（ppm）', y='AQI', data=aqi, hue='质量等级')
plt.title('AQI与PM2.5关系散点图')
plt.savefig('scatter_aqi_pm2.5.png')
plt.show()

# 分类散点图
plt.figure(figsize=(12, 8))
sns.stripplot(x='质量等级', y='AQI', data=aqi, jitter=True)
plt.title('空气质量分类散点图')
plt.savefig('strip_quality.png')
plt.show()

# 分布图
plt.figure(figsize=(12, 8))
sns.displot(aqi['AQI'], kde=True)
plt.title('AQI分布图')
plt.savefig('dist_aqi.png')
plt.show()

# 回归图
plt.figure(figsize=(12, 8))
sns.regplot(x='PM2.5含量（ppm）', y='AQI', data=aqi)
plt.title('PM2.5与AQI线性回归')
plt.savefig('reg_pm2.5_aqi.png')
plt.show()

# 任务三实训2
# 计算相关系数
corr = aqi[['AQI','PM2.5含量（ppm）','PM10含量（ppm）','SO2含量（ppm）','CO含量（ppm）','NO2含量（ppm）','O3_8h含量（ppm）']].corr()

# 热力图
plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('空气质量指标相关性热力图')
plt.savefig('heatmap_correlation.png')
plt.show()