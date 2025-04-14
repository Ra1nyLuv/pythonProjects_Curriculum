import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

# 读取数据（复用task3.py中的数据）
data = {
    '年份': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008],
    '第一产业就业人员（万人）': [36042.5, 36398.5, 36640, 36204.4, 34829.8, 33441.9, 31940.6, 30731, 29923.3],
    '第二产业就业人员（万人）': [16219.1, 16233.7, 15681.9, 15927, 16709.4, 17766, 18894.5, 20186, 20553.4],
    '第三产业就业人员（万人）': [19823.4, 20164.8, 20958.1, 21604.6, 22724.8, 23439.2, 24142.9, 24404, 25087.2]
}
df = pd.DataFrame(data)

# 设置绘图
fig, ax = plt.subplots(figsize=(10, 6))
years = df['年份']
bar_width = 0.2
positions = range(len(years))

# 初始化条形图
bars1 = ax.bar(positions, df['第一产业就业人员（万人）'], bar_width, label='第一产业')
bars2 = ax.bar([p + bar_width for p in positions], df['第二产业就业人员（万人）'], bar_width, label='第二产业')
bars3 = ax.bar([p + 2 * bar_width for p in positions], df['第三产业就业人员（万人）'], bar_width, label='第三产业')

# 设置标题和标签
ax.set_title('2000-2008年各产业就业人员动态条形图')
ax.set_xlabel('年份')
ax.set_ylabel('就业人员数量（万人）')
ax.set_xticks([p + bar_width for p in positions])
ax.set_xticklabels(years)
ax.legend()

# 更新函数
def update(frame):
    # 更新每个条形的高度
    for bar, height in zip(bars1, df.iloc[:frame + 1]['第一产业就业人员（万人）']):
        bar.set_height(height)
    for bar, height in zip(bars2, df.iloc[:frame + 1]['第二产业就业人员（万人）']):
        bar.set_height(height)
    for bar, height in zip(bars3, df.iloc[:frame + 1]['第三产业就业人员（万人）']):
        bar.set_height(height)
    return bars1, bars2, bars3

# 创建动画
ani = FuncAnimation(fig, update, frames=len(years), interval=1000, blit=False)

# 显示动画
plt.show()