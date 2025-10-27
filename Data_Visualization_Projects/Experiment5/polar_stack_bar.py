from pyecharts import options as opts
from pyecharts.charts import Bar
import pandas as pd

# 解决中文显示问题
import sys
import os
sys.path.append(os.path.abspath('.'))

# 读取高校数据
try:
    df = pd.read_csv(r'Experiment5\colleges_universities.csv', encoding='gbk')
except:
    df = pd.read_csv(r'Experiment5\colleges_universities.csv', encoding='utf-8')

# 提取省份和本专科数据
provinces = df['省份'].tolist()
undergrad = df['本科'].tolist()
college = df['专科'].tolist()

# 创建堆叠柱形图
bar = (Bar()
    .add_xaxis(provinces)
    .add_yaxis("本科", undergrad, stack='stack1')
    .add_yaxis("专科", college, stack='stack1')
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各省高校数量分布", subtitle="数据来源: colleges_universities.csv"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
        yaxis_opts=opts.AxisOpts(name="院校数量"),
        toolbox_opts=opts.ToolboxOpts()
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
    ))

# 生成HTML文件
bar.render("./colleges_stacked_bar.html")
