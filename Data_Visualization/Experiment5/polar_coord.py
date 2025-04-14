from pyecharts import options as opts
from pyecharts.charts import Polar
import pandas as pd
import os
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取高校数据
try:
    df = pd.read_csv('colleges_universities.csv', encoding='gbk')
except:
    df = pd.read_csv('colleges_universities.csv', encoding='utf-8')

# 处理数据
provinces = df['省份'].tolist()
undergrad = df['本科'].tolist()
college = df['专科'].tolist()

# 创建极坐标堆叠柱形图
polar = (
    Polar()
    .add_schema(
        radiusaxis_opts=opts.RadiusAxisOpts(data=provinces, type_="category"),
        angleaxis_opts=opts.AngleAxisOpts(is_clockwise=True)
    )
    .add("本科院校", undergrad, type_="bar", stack="stack1")
    .add("专科院校", college, type_="bar", stack="stack1")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各省高校极坐标分布"),
        toolbox_opts=opts.ToolboxOpts(),
        legend_opts=opts.LegendOpts(pos_left="80%")
    )
)

# 生成HTML文件
polar.render("./polar_stack_chart.html")
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False