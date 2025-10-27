import pandas as pd
import numpy as np
from pyecharts.charts import Line, Pie, Bar
from pyecharts import options as opts
from datetime import datetime
import chardet


# 1. 数据清洗
def data_cleaning(file_path):
    # 检测文件编码
    def detect_encoding(file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']

    # 检测并读取文件
    file_encoding = detect_encoding(file_path)
    print(f"Detected file encoding: {file_encoding}")
    df = pd.read_csv(file_path, encoding=file_encoding)

    # 删除重复列
    df = df.loc[:, ~df.columns.duplicated()]

    # 删除记录重复值
    df.drop_duplicates(inplace=True)

    # 删除缺失值
    df.dropna(inplace=True)

    # 转换日期字段为 datetime 格式
    df['销售日期'] = pd.to_datetime(df['销售日期'], format='%Y%m%d', errors='coerce')

    # 将 "是否促销" 列转换为布尔值
    df['是否促销'] = df['是否促销'].map({'是': True, '否': False})

    # 检查销售日期是否正确解析
    print("销售日期样本：\n", df['销售日期'].head())

    return df


# 2. 数据统计
def data_statistics(df):
    # (1) 统计各大类商品的销售金额
    category_sales = df.groupby('大类名称')['销售金额'].sum().reset_index()

    # (2) 统计各中类商品的促销销售金额和非促销销售金额（按销售周分组）
    df['销售周'] = df['销售日期'].dt.isocalendar().week

    promotion_sales = (
        df.groupby(['销售周', '中类名称', '是否促销'])['销售金额']
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )

    # 重命名 unstack 后的列
    promotion_sales.rename(columns={True: '促销', False: '非促销'}, inplace=True)

    # 打印 promotion_sales 数据框的列名和前几行
    print("promotion_sales 列名：", promotion_sales.columns.tolist())
    print("promotion_sales 前几行：\n", promotion_sales.head())

    # (3) 统计生鲜类产品和一般产品的每周销售金额
    product_type_weekly_sales = df.groupby(['商品类型', '销售周'])['销售金额'].sum().reset_index()

    # (4) 统计每位顾客每月的消费额及消费天数
    df['销售月份'] = df['销售日期'].dt.month
    customer_monthly_stats = df.groupby(['顾客编号', '销售月份']).agg(
        消费额=('销售金额', 'sum'),
        消费天数=('销售日期', 'nunique')
    ).reset_index()

    return category_sales, promotion_sales, product_type_weekly_sales, customer_monthly_stats


# 3. 数据分析与可视化
def data_visualization(category_sales, promotion_sales, product_type_weekly_sales, customer_monthly_stats):
    # (1) 生鲜类商品和一般商品每天销售金额折线图
    daily_sales = product_type_weekly_sales.groupby(['商品类型', '销售周'])['销售金额'].sum().reset_index()
    line_chart = (
        Line()
        .add_xaxis(daily_sales['销售周'].unique().tolist())
        .add_yaxis("生鲜类", daily_sales[daily_sales['商品类型'] == '生鲜']['销售金额'].tolist())
        .add_yaxis("一般商品", daily_sales[daily_sales['商品类型'] == '一般商品']['销售金额'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="每日销售金额"))
    )
    line_chart.render("daily_sales.html")

    # (2) 按月绘制各大类商品销售金额的占比饼图
    pie_charts = []
    for month in customer_monthly_stats['销售月份'].unique():
        monthly_data = category_sales.copy()  # 使用 category_sales 数据框
        pie_chart = (
            Pie()
            .add("", [list(z) for z in zip(monthly_data['大类名称'], monthly_data['销售金额'])])
            .set_global_opts(title_opts=opts.TitleOpts(title=f"第{month}月销售金额占比"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        pie_charts.append(pie_chart)

    # 将所有饼图合并成大屏展示
    combined_pie_chart = (
        Pie()
        .add("", [list(z) for z in zip(category_sales['大类名称'], category_sales['销售金额'])])
        .set_global_opts(title_opts=opts.TitleOpts(title="月度销售金额占比大屏"))
    )
    combined_pie_chart.render("combined_pie_chart.html")

    # (3) 促销商品和非促销商品销售金额的周环比增长率柱状图
    weekly_promotion_sales = promotion_sales.groupby('销售周')[['促销', '非促销']].sum().reset_index()
    weekly_promotion_sales['周环比增长率'] = weekly_promotion_sales['促销'].pct_change() * 100
    bar_chart = (
        Bar()
        .add_xaxis(weekly_promotion_sales['销售周'].tolist())
        .add_yaxis("周环比增长率", weekly_promotion_sales['周环比增长率'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="促销商品周环比增长率"))
    )
    bar_chart.render("weekly_growth_rate.html")


# 主函数
if __name__ == "__main__":
    file_path = "某超市的销售数据.csv"

    # 数据清洗
    cleaned_data = data_cleaning(file_path)

    # 数据统计
    category_sales, promotion_sales, product_type_weekly_sales, customer_monthly_stats = data_statistics(cleaned_data)

    # 数据可视化
    data_visualization(category_sales, promotion_sales, product_type_weekly_sales, customer_monthly_stats)