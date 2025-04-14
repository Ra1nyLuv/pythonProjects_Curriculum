from pyecharts import options as opts
from pyecharts.charts import Calendar
import datetime
import os

# 文件路径配置
current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, 't_alibaba_data3.txt')

# 读取并处理数据
data_dict = {}
valid_count = 0
total_lines = 0
with open(data_file, 'r', encoding='utf-8') as f:
    for line in f:
        total_lines += 1
        line = line.strip()
        if not line:
            continue
        parts = line.strip().split('\t')
        if len(parts) >=4:
            date_str = f'2020-{parts[3].replace("/", "-")}'
            try:
                datetime.datetime.strptime(date_str, '%Y-%m-%d')
                if parts[2] == '3':
                    data_dict[date_str] = data_dict.get(date_str, 0) + 1
                    valid_count += 1
                    if valid_count <= 5:
                        print(f"样本记录：日期={date_str}, 类型={parts[2]}")
            except ValueError:
                print(f"第{total_lines}行日期格式错误: {parts[3]}")

print(f"共处理{total_lines}行数据，其中有效消费记录{valid_count}条")

if not data_dict:
    raise ValueError("未找到有效的消费数据，请检查数据文件格式和过滤条件")

# 转换为日历图所需格式
calendar_data = [
    [dt, count]
    for dt, count in sorted(data_dict.items(), key=lambda x: x[0])
]

# 创建日历热力图
calendar = (
    Calendar(init_opts=opts.InitOpts(width='1200px', height='800px'))
    .add(
        series_name='消费次数',
        data=calendar_data,
        calendar_opts=opts.CalendarOpts(
            range_=['2020-01-01', '2020-12-31'],
            daylabel_opts=opts.CalendarDayLabelOpts(name_map='cn'),
            monthlabel_opts=opts.CalendarMonthLabelOpts(name_map='cn'),
        ),
        # 新增y轴数据配置
        yaxis_data=calendar_data
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title='2020年天猫消费行为日历热力图',
            subtitle='数据来源: t_alibaba_data3.txt',
            pos_left='center'
        ),
        visualmap_opts=opts.VisualMapOpts(
            max_=max(data_dict.values()),
            min_=0,
            orient='horizontal',
            is_piecewise=True,
            pos_top='50px',
            pos_left='center'
        ),
        tooltip_opts=opts.TooltipOpts(trigger='item')
    )
)

# 保存结果
output_path = os.path.join(current_dir, 'calendar_heatmap.html')
calendar.render(output_path)
print(f'日历热力图已生成至: {output_path}')