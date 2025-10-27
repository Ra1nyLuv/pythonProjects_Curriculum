from pyecharts import options as opts
from pyecharts.charts import Calendar
import datetime
import os

# 文件路径配置
current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, 't_alibaba_data4.txt')

# 初始化存储结构
behavior_dict = {
    '0': '浏览',
    '2': '收藏',
    '3': '购买',
    '4': '购物车'
}
daily_counts = {dt: {bt:0 for bt in behavior_dict} for dt in [datetime.date(2020, m, d).strftime('%Y-%m-%d') 
    for m in range(1,13) for d in range(1,32) if datetime.date(2020,m,d).month == m]}

# 读取并处理数据
with open(data_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >=4 and parts[2] in behavior_dict:
            date_str = f"2020-{parts[3].replace('/', '-')}"  # 转换06/04为2020-06-04
            try:
                datetime.datetime.strptime(date_str, '%Y-%m-%d')
                daily_counts[date_str][parts[2]] += 1
            except:
                continue

# 生成日历图数据
calendar_data = [
    [dt, sum(counts.values())]
    for dt, counts in daily_counts.items()
]

# 创建日历热力图
calendar = (
    Calendar(init_opts=opts.InitOpts(width='1200px', height='800px'))
    .add(
        series_name='用户行为密度',
        data=calendar_data,
        calendar_opts=opts.CalendarOpts(
            range_=['2020-01-01', '2020-12-31'],
            daylabel_opts=opts.CalendarDayLabelOpts(name_map='cn'),
            monthlabel_opts=opts.CalendarMonthLabelOpts(name_map='cn')
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title='2020年天猫用户行为日历热力图',
            subtitle='数据格式: 用户ID\t商品ID\t行为类型\t日期',
            pos_left='center'
        ),
        visualmap_opts=opts.VisualMapOpts(
            max_=max([d[1] for d in calendar_data]),
            min_=0,
            orient='horizontal',
            is_piecewise=True,
            pos_top='50px',
            pos_left='center'
        )
    )
)

# 保存结果
output_path = os.path.join(current_dir, 'user_behavior_calendar.html')
calendar.render(output_path)
print(f'用户行为日历热力图已生成至: {output_path}')