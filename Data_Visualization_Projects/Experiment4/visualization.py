import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']

# 修正文件路径转义
try:
    df = pd.read_csv(r'Experiment4\hr.csv', encoding='gbk')
except:
    df = pd.read_csv(r'Experiment4\hr.csv', encoding='utf-8')

# 筛选所需列并转换类型
data = df[['每月平均工作小时数（小时）', '满意度', '薪资', '评分', '部门']].copy()
data['部门'] = data['部门'].astype('category')

# 创建可视化图表
plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=data,
    x='每月平均工作小时数（小时）',
    y='满意度',
    hue='薪资',
    size='评分',
    style='部门',
    palette='viridis',
    sizes=(30, 200),
    alpha=0.7
)

# 优化图表显示
plt.title('多维数据分析 - 工时 vs 满意度')
plt.xlabel('每月平均工作小时数（小时）（小时）')
plt.ylabel('员工满意度')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('multidimensional_plot.png')
plt.show()

# 任务一验证代码
# 验证'muted'调色板效果
data = df.head(100)
plt.figure(figsize=(15, 8))
sns.scatterplot(x='每月平均工作小时数（小时）', y='满意度', data=data, hue='薪资', size='工龄（年）', palette='muted', style='薪资')
plt.xlabel('平均每个月工作时长（小时）')
plt.ylabel('满意度水平')
plt.title('muted调色板效果')
plt.savefig('muted_palette.png')
plt.show()

# 验证bright调色板
plt.figure(figsize=(15, 8))
pal_hex = sns.color_palette("bright",3).as_hex()
sns.scatterplot(x='每月平均工作小时数（小时）', y='满意度', data=data, hue='薪资', size='薪资', sizes=(200,50), palette=pal_hex)
plt.title('bright调色板效果')
plt.savefig('bright_palette.png')
plt.show()

# 元素缩放实验
sns.set()
x = np.arange(1, 10, 2)
y1 = x + 1
y2 = x + 3
y3 = x + 5

def showLine(flip=1):
    sns.lineplot(x=x, y=y1)
    sns.lineplot(x=x, y=y2)
    sns.lineplot(x=x, y=y3)

plt.figure(figsize=(8, 8))
plt.subplot(2,2,1)
with sns.plotting_context('paper'):
    showLine()
    plt.title('paper')

# 补全子图配置
plt.subplot(2,2,2)
with sns.plotting_context('notebook'):
    showLine()
    plt.title('notebook')

plt.subplot(2,2,3)
with sns.plotting_context('talk'):
    showLine()
    plt.title('talk')

plt.subplot(2,2,4)
with sns.plotting_context('poster'):
    showLine()
    plt.title('poster')
plt.show()
