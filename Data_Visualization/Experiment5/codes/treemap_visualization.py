from pyecharts import options as opts
from pyecharts.charts import TreeMap
import json
import os


current_dir = os.path.dirname(os.path.abspath(__file__))

# 读取GDP数据
with open(r'Experiment5/GDP_data_1.json', 'r', encoding='utf-8') as f:
    gdp_data = json.load(f)

# 创建矩形树图
tree = (
    TreeMap()
    .add("GDP分布",
        data=gdp_data,
        levels=[
            opts.TreeMapLevelsOpts(
                treemap_itemstyle_opts=opts.TreeMapItemStyleOpts(
                    border_color="#555",
                    border_width=4,
                    gap_width=2
                )
            ),
            opts.TreeMapLevelsOpts(
                color_saturation=[0.3, 0.6],
                treemap_itemstyle_opts=opts.TreeMapItemStyleOpts(
                    border_color="#ddd",
                    border_width=2,
                    gap_width=1
                )
            )
        ]
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="GDP分布矩形树图", subtitle="数据来源: GDP_data_1.json"),
        toolbox_opts=opts.ToolboxOpts()
    )
)

tree.render(os.path.join(current_dir, "./gdp_treemap.html"))