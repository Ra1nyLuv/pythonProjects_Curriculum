import schedule
import os
from bs4 import BeautifulSoup
import requests
import re
from time import localtime, sleep
import pyttsx3
import webbrowser
import markdown
from pyecharts.charts import Line
from pyecharts import options as opts
import pandas as pd
import csv
from lxml import etree
import demjson

# 爬取未来七天天气数据
def future_weather():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        }
        response = requests.get(url=url, headers=headers)
        resp_html = etree.HTML(response.text)

        # 提取未来七天的数据
        daysData_script = resp_html.xpath("//script[contains(text(), 'var daysData =')]/text()")[0]
        daysData_text = daysData_script.split('=', 1)[1].strip().rstrip(';')
        # print(f"daysData_text: {daysData_text}")


        # 使用demjson解析数据
        daysData = demjson.decode(daysData_text)
        # print(f"daysData: {daysData}")

        data = []
        for i in range(7):
            entry = {
                '时间': daysData['date'][i],
                '日间天气': daysData['weather1'][i],
                '夜间天气': daysData['weather2'][i],
                '最高温': daysData['seriesData1'][i],
                '最低温': daysData['seriesData2'][i]
            }
            data.append(entry)

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as f:
            csv_writer = csv.DictWriter(f, fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)

    except requests.exceptions.ConnectionError as e:
        print("网络请求发生异常,请检查网络连接...\n若依然无法运行,请检查'url'变量...\n", e)
        exit()

def weather_view():
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    week_name_list = df['时间'].tolist()
    high_temperature = df['最高温'].tolist()  # 直接转换为列表
    low_temperature = df['最低温'].tolist()   # 直接转换为列表

    # 移除或调整以下的检查逻辑，因为我们已经知道数据是int类型
    # 遍历数据，将None替换为空字符串或其他默认值，如果需要的话
    high_temperature = [temp if pd.notna(temp) else None for temp in high_temperature]
    low_temperature = [temp if pd.notna(temp) else None for temp in low_temperature]

    line_chart = (
        Line()
        .add_xaxis(xaxis_data=week_name_list)
        .add_yaxis(
            series_name="最高气温",
            y_axis=high_temperature,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
            linestyle_opts=opts.LineStyleOpts(color='red', width=2)
        )
        .add_yaxis(
            series_name="最低气温",
            y_axis=low_temperature,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(type_="max", name="最大值")]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
            linestyle_opts=opts.LineStyleOpts(color='blue', width=2)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="未来一周气温变化", subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(font_size=14),
                pos_top='5%'
            )
        )
    )
    chart_html = line_chart.render_embed()
    return chart_html

# 获取实时天气数据
def get_data():
    try:
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, 'html.parser')
        return str(soup)
    except requests.exceptions.ConnectionError as e:
        print("网络请求发生异常,请检查网络连接...\n若依然无法运行,请检查'url'变量...\n", e)
        exit()

# 整合处理数据, 并根据传入的数据生成天气报告的文本
def process_data():
    data = get_data()
    result = {
        '湿度': None,
        '风向': None,
        '空气质量': None,
        '紫外线': None,
        '平均温度': None,
        '最低温': None,
        '最高温': None,
        '日间天气': None,
        '夜间天气': None,
        '日期': f"{localtime().tm_year}年{localtime().tm_mon}月{localtime().tm_mday}日{localtime().tm_hour}时{localtime().tm_min}分"
    }

    # 正则表达式匹配
    s1 = re.compile(r'\d+%')
    s2 = re.compile(r'\w{1,4}风\s*\d{1,2}级')
    s3 = re.compile(r'空气：\w+\s*\d{1,2}')
    s4 = re.compile(r'紫外线 \w{1,2}')
    s5 = re.compile(r'平均温度：\d{1,2} ~ \d{1,2}°C')
    s6 = re.compile(r'最低温（\d{1,2}°）')
    s7 = re.compile(r'最高温（\d{1,2}°）')
    s8 = re.search(r'<dd class="txt">(.*?)</dd>', data)

    # 提取数据
    result['湿度'] = s1.search(data).group() if s1.search(data) else None
    result['风向'] = s2.search(data).group() if s2.search(data) else None
    result['空气质量'] = s3.search(data).group() if s3.search(data) else None
    result['紫外线'] = s4.search(data).group() if s4.search(data) else None
    result['平均温度'] = s5.search(data).group() if s5.search(data) else None
    result['最低温'] = s6.search(data).group().replace('(', '').replace(')', '') if s6.search(data) else None
    result['最高温'] = s7.search(data).group().replace('(', '').replace(')', '') if s7.search(data) else None

    # 处理天气状况数据
    if s8:
        weather_text = s8.group(1)
        if '/' in weather_text:
            day_weather, night_weather = weather_text.split('/')
            result['日间天气'] = day_weather.strip()
            result['夜间天气'] = night_weather.strip()
        else:
            result['日间天气'] = weather_text.strip()
            result['夜间天气'] = weather_text.strip()

    # 构建天气报告文本
    result_text_ls = [
        "## 您好，我是您的天气小助手(●_●)\n",
        "### 您的今日天气报告已生成:\n\n\n",
        f"现在是**{result['日期']}**, \n" if result['日期'] else "",
        f"今天的日间天气状况为**{result['日间天气']}**,\n" if result['日间天气'] else "",
        f"今天的夜间天气状况为**{result['夜间天气']}**,\n" if result['夜间天气'] else "",
        f"**{result['空气质量']}**,  湿度为**{result['湿度']}**,\n" if result['空气质量'] and result['湿度'] else "",
        f"风向为**{result['风向']}**, \n" if result['风向'] else "",
        f"紫外线强度**{result['紫外线'][4:7]}**, \n" if result['紫外线'] else "",
        f"\n今日**{result['平均温度']}**, \n**{result['最高温']}**，**{result['最低温']}**.\n\n" if all([result['平均温度'], result['最高温'], result['最低温']]) else ""
    ]

    # 根据天气状况添加一些小贴士
    if "晴" in (result['日间天气'] or "") or "晴" in (result['夜间天气'] or ""):
        result_text_ls.append("**今天天气晴朗，适合户外活动.**\n")
        if int(re.sub('[^0-9]', '', result['最高温'])) >= 28:
            result_text_ls.append("**天气炎热，请注意防暑,做好防晒.**")
    elif "雨" in (result['日间天气'] or "") or "雨" in (result['夜间天气'] or ""):
        result_text_ls.append("**今天有雨,尽量减少户外出行.**\n")
        if "大雨" in (result['日间天气'] or "") or "大雨" in (result['夜间天气'] or ""):
            result_text_ls.append("**降雨强度较大，尽量避免外出，确保安全.**")
        else:
            result_text_ls.append("**外出时请小心滑倒.**")
    elif "雪" in (result['日间天气'] or "") or "雪" in (result['夜间天气'] or ""):
        result_text_ls.append("**今天可能会有雪，注意保暖.\n外出时请小心行走，避免滑倒.**")
    else:
        result_text_ls.append("**今天天气变化多端，请注意身体，小心感冒.**")

    result_text_ls.append("\n\n> 天气小助手(●_●)希望您度过美好的一天'^-^'")
    return [line for line in result_text_ls if line.strip()]

# 将处理好的数据文本传入后,写入文件并设置朗读功能
def write_file():
    result_text_ls = process_data()

    def read_report():
        if set_read:
            engine = pyttsx3.init()
        
            # 原始文本拼接
            text = ''.join(result_text_ls).replace('\\n', '\n').replace('_', '')
            
            # 先替换温度符号和区间符号
            text = text.replace('°C', '度').replace('~', '至')

            # 按行分割文本
            lines = text.splitlines()
            new_lines = []
            for line in lines:
                if line.strip():  # 判断该行是否为空行，strip去除两端空白字符后如果为空则是原空行
                    # 使用更精准的正则表达式，保留数字、汉字、逗号、特定符号及单位等
                    processed_line = re.sub(r"[^\u4e00-\u9fff0-9,\:\°\·\s\(\)“”%【】]+", "", line)
                    new_lines.append(processed_line)
                else:
                    new_lines.append(",")

            # 重新组合处理后的行
            text = "".join(new_lines)

            # print(f"text: {text}")
            engine.say(text)
            engine.runAndWait()

    try:
        with open(report_path, "w", encoding='utf-8') as file:
            for i in result_text_ls:
                file.write(i)

        convert_md_to_html(report_path, report_html_path)

        print('\n--您的报告已生成, 请到桌面查看^^_')

        print("""\ntips:若要查看其他城市的天气,
        将'url'网址最后的/putian/ 改为需要查看的城市名的英文拼写即可
                如'https://www.tianqi24.com/fuzhou/'.""")

        read_report()

    except FileNotFoundError as e:
        print("目标文件路径不存在, 请修改'report_path'后重试...\n", e)
        exit()

# 将Markdown文件转换为HTML文件，并嵌入温度趋势图
def convert_md_to_html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content)

    # 生成温度趋势图
    chart_html = weather_view()

    # 定义HTML模板，包括浅色背景和居中的CSS样式
    html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>每日天气报告</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #F0F0F0; /* 设置浅色背景 */
        }}

       .container {{
            text-align: center;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
            max-width: 800px; /* 设置最大宽度 */
            width: 100%; /* 确保容器适应屏幕大小 */
            margin: 20px auto; /* 确保容器在页面中间 */
        }}

       .container h1,.container h2,.container p {{
            margin: 10px 0;
        }}

       .chart-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }}

       .chart-container canvas {{
            max-width: 100%;
            height: auto;
        }}

       .container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        .copyright {{
            padding: 10px 0 7px 0;
            font-family: "Raleway", sans-serif;
            font-size: 13px;
            transparent: 0.8;
            color: grey;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
        <h2>未来一周温度趋势图</h2>
        <div class="chart-container">
            {chart_html} <!-- 插入图表的HTML -->
        </div>
            <div class="copyright">
                Copyright &copy; 2024. <br>莆田学院 新工科产业学院 数据225 14组 <br> All rights reserved.
            </div>
    </div>
</body>
</html>
"""

    # 使用模板生成完整的HTML文档
    complete_html = html_template.format(html_content=html_content, chart_html=chart_html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(complete_html)

# 使用默认浏览器打开HTML文件
def open_html_in_browser(html_path):
    if not os.path.exists(html_path):
        print(f"文件 {html_path} 不存在")
        return
    webbrowser.open('file://' + os.path.realpath(html_path))

# 定时启动功能, 可设定每天某个时间自动执行一次
def execute_on_time(due_time):
    schedule.every().day.at(due_time).do(get_started)

    while True:
        schedule.run_pending()
        sleep(1)

# 启动
def get_started():
    # 更新未来七天的天气数据
    future_weather()

    if not set_run_time:
        write_file()
        open_html_in_browser(report_html_path)
    else:
        execute_on_time(due_time)

# 全局变量
csv_file_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'weather_data.csv')
report_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'Daily_Weather_Report.md')
report_html_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'Daily_Weather_Report.html')

# 爬取天气数据的目标网址
url = "https://www.tianqi24.com/fuzhou/"

# 若要使用朗读功能,将set_read设置为True即可.
set_read = False

# 若要使用定时功能,将set_run_time设置为True即可.
set_run_time = False

# 若要调整指定执行时间, 请在将"set_run_time"设为True后,修改due_time, 格式为'hh:mm'(24h制).
due_time = '07:00'

# 启动程序
get_started()
