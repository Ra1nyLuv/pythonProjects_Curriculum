import pandas as pd
import matplotlib.pyplot as plt

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
data1 = pd.read_csv("数据1.csv", encoding="gbk")
data2 = pd.read_csv("数据2.csv", encoding="gbk")

# 合并数据
merged_data = pd.merge(data1, data2, left_on="商品", right_on="商品", how="inner")
merged_data.to_csv("合并后的数据.csv", index=False, encoding="utf-8")

# 数据校验与清洗
# （1）查找重复记录并删除
duplicates = merged_data[merged_data.duplicated()]
print("重复记录数量：", len(duplicates))
cleaned_data = merged_data.drop_duplicates()

# （2）查找异常数据，并在箱线图中绘制处理，最后对异常数据进行删除
# 检查“实际金额”列的数据类型和内容
print("数据类型：", cleaned_data["实际金额"].dtype)
print("前几行数据：\n", cleaned_data["实际金额"].head())

# 将“实际金额”列转换为数值类型，无法转换的值设置为 NaN
cleaned_data["实际金额"] = pd.to_numeric(cleaned_data["实际金额"], errors="coerce")

# 删除包含 NaN 的行
cleaned_data = cleaned_data.dropna(subset=["实际金额"])

# 再次检查数据类型和内容
print("转换后的数据类型：", cleaned_data["实际金额"].dtype)
print("转换后的前几行数据：\n", cleaned_data["实际金额"].head())

# 计算四分位数和异常值范围
Q1 = cleaned_data["实际金额"].quantile(0.25)
Q3 = cleaned_data["实际金额"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
cleaned_data = cleaned_data[(cleaned_data["实际金额"] >= lower_bound) & (cleaned_data["实际金额"] <= upper_bound)]

# （3）查找缺失值并处理（删除、填充等）
missing_values = cleaned_data.isnull().sum()
print("缺失值统计：\n", missing_values)

# 使用前向填充处理缺失值
cleaned_data.ffill(inplace=True)

# （4）处理“支付时间”列
# 检查支付时间列的前几行
print("支付时间列前几行：\n", cleaned_data["支付时间"].head())

# 去除多余的 ":00"
cleaned_data["支付时间"] = cleaned_data["支付时间"].str.replace(":00$", "", regex=True)

# 转换为 datetime 类型
cleaned_data["支付时间"] = pd.to_datetime(cleaned_data["支付时间"], format="%Y/%m/%d %H:%M", errors="coerce")

# 删除无法解析的时间数据
cleaned_data = cleaned_data.dropna(subset=["支付时间"])

# 保存处理后的数据
cleaned_data.to_csv("清洗后的数据.csv", index=False, encoding="utf-8")

# 数据分析与可视化
# （1）绘制每个月的订单量柱状图
monthly_orders = cleaned_data.groupby(cleaned_data["支付时间"].dt.to_period("M")).size()

plt.figure(figsize=(10, 6))
monthly_orders.plot(kind="bar", color="skyblue")
plt.title("每月订单量")
plt.xlabel("月份")
plt.ylabel("订单量")
plt.show()

# （2）绘制每个月的销售额变化折线图
monthly_sales = cleaned_data.groupby(cleaned_data["支付时间"].dt.to_period("M"))["实际金额"].sum()

plt.figure(figsize=(10, 6))
monthly_sales.plot(kind="line", marker="o", color="orange")
plt.title("每月销售额变化")
plt.xlabel("月份")
plt.ylabel("销售额")
plt.grid()
plt.show()

# （3）绘制 A 类自动售货机中“怡宝纯净水”的商品 12 个月订单量饼图
filtered_data = cleaned_data[(cleaned_data["设备ID"] == "E43A6E078A04172") & (cleaned_data["商品"] == "怡宝纯净水")]
monthly_water_orders = filtered_data.groupby(filtered_data["支付时间"].dt.month).size()

plt.figure(figsize=(8, 8))
monthly_water_orders.sort_values(ascending=False).plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("A 类售货机 - 怡宝纯净水月订单量分布")
plt.ylabel("")
plt.show()

# （4）对五类自动售货机的实付金额数据，分别绘制出箱线图
grouped_data = [cleaned_data[cleaned_data["设备ID"] == machine]["实际金额"] for machine in ["E43A6E078A04172", "E43A6E078A04134", "E43A6E078A04228", "E43A6E078A07631", "E43A6E078A06874"]]

plt.figure(figsize=(10, 6))
plt.boxplot(grouped_data, labels=["A", "B", "C", "D", "E"], vert=False)
plt.title("五类自动售货机实付金额分布")
plt.xlabel("实付金额")
plt.show()