import pandas as pd
import numpy as np
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts


# 1. 数据清洗和预处理
def preprocess_data(df):
    # 将 "是否促销" 列转换为布尔值
    df['是否促销'] = df['是否促销'].map({'是': True, '否': False})

    # 确保日期字段为 datetime 格式
    df['销售日期'] = pd.to_datetime(df['销售日期'], format='%Y%m%d', errors='coerce')
    df['销售月份'] = df['销售日期'].dt.month

    return df


# 2. 累计消费前10名顾客画像
def customer_profile(df, top_n=10):
    # 按累计消费额排序选出前10名顾客
    top_customers = df.groupby('顾客编号')['销售金额'].sum().nlargest(top_n).index
    top_customer_data = df[df['顾客编号'].isin(top_customers)].copy()

    # 分析前10名顾客的消费偏好
    customer_profile = top_customer_data.groupby(['顾客编号', '大类名称'])['销售金额'].sum().reset_index()
    print("前10名顾客消费偏好：\n", customer_profile)

    # 按商品类型统计消费金额和数量
    product_preference = (
        top_customer_data.groupby(['顾客编号', '商品编码'])[['销售金额', '销售数量']]
        .sum()
        .reset_index()
    )
    print("前10名顾客商品偏好：\n", product_preference)

    # 按月份统计消费金额
    monthly_consumption = (
        top_customer_data.groupby(['顾客编号', '销售月份'])['销售金额'].sum().reset_index()
    )

    # 可视化：前10名顾客每月消费金额折线图
    line_chart = (
        Line()
        .add_xaxis(monthly_consumption['销售月份'].unique().tolist())
    )
    for customer in top_customers:
        customer_monthly = monthly_consumption[monthly_consumption['顾客编号'] == customer]
        line_chart.add_yaxis(
            f"顾客{customer}",
            customer_monthly['销售金额'].tolist(),
            is_smooth=True
        )
    line_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="前10名顾客每月消费金额"),
        xaxis_opts=opts.AxisOpts(name="月份"),
        yaxis_opts=opts.AxisOpts(name="消费金额")
    )
    line_chart.render("top_customers_monthly_consumption.html")


# 3. 分析各大类商品的销售情况
def category_sales_analysis(df):
    # 按大类统计销售金额
    category_sales = df.groupby('大类名称')['销售金额'].sum().reset_index()

    # 按月统计各大类商品的销售金额
    monthly_category_sales = (
        df.groupby(['销售月份', '大类名称'])['销售金额']
        .sum()
        .reset_index()
    )

    # 可视化：各大类商品月度销售金额柱状图
    bar_chart = (
        Bar()
        .add_xaxis(category_sales['大类名称'].tolist())
    )
    for month in monthly_category_sales['销售月份'].unique():
        monthly_data = monthly_category_sales[monthly_category_sales['销售月份'] == month]
        bar_chart.add_yaxis(
            f"{month}月",
            monthly_data['销售金额'].tolist(),
            stack="stack1"
        )
    bar_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="各大类商品月度销售金额"),
        xaxis_opts=opts.AxisOpts(name="大类名称"),
        yaxis_opts=opts.AxisOpts(name="销售金额")
    )
    bar_chart.render("category_monthly_sales.html")


# 4. 分析促销对商品的影响
def promotion_analysis(df):
    # 按促销状态统计销售金额
    promotion_effect = df.groupby('是否促销')['销售金额'].sum().reset_index()

    # 可视化：促销与非促销商品销售金额对比饼图
    pie_chart = (
        Pie()
        .add("", [list(z) for z in zip(promotion_effect['是否促销'], promotion_effect['销售金额'])])
        .set_global_opts(title_opts=opts.TitleOpts(title="促销对商品销售金额的影响"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie_chart.render("promotion_effect_pie.html")


# 主函数
if __name__ == "__main__":
    file_path = "某超市的销售数据.csv"
    df = pd.read_csv(file_path, encoding = 'gbk')
    df = preprocess_data(df)

    # 1. 累计消费前10名顾客画像
    customer_profile(df)

    # 2. 分析各大类商品的销售情况
    category_sales_analysis(df)

    # 3. 分析促销对商品的影响
    promotion_analysis(df)