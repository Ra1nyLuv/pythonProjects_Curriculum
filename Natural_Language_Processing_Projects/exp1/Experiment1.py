# 自然语言处理-实验一

def build_dictionary():
    dictionary = [
        "过去", "的一年", "是", "我国", "社会主义", "改革开放", "和", "现代化建设",
        "进程", "中", "具有", "标志", "意义", "的", "一年", "在", "中国共产党", "领导",
        "下", "全国", "各族", "人民", "团结", "奋斗", "国民经济", "继续", "保持", "较快",
        "发展", "势头", "经济结构", "战略性", "调整", "顺利", "部署", "实施", "西部大开发",
        "取得", "良好", "开端", "精神文明", "建设", "民主", "法制", "进一步", "加强",
        "我们", "在", "过去", "几年", "取得", "成绩", "的", "基础上", "胜利", "完成",
        "第九个五年计划", "我国", "已", "进入", "了", "全面", "建设", "小康社会",
        "加快", "社会主义", "现代化", "新的", "发展阶段"
    ]
    return dictionary

def forward_maximum_matching(text, dictionary):
    max_length = max(len(word) for word in dictionary) 
    result = []  
    start = 0  

    while start < len(text):
        matched = False  
        for length in range(max_length, 0, -1): 
            if start + length > len(text): 
                continue
            word = text[start:start + length] 
            if word in dictionary:  
                result.append(word)
                matched = True
                start += length 
                break
        if not matched:  
            result.append(text[start])
            start += 1

    return result

# 测试数据
test_data = (
    "过去的一年，是我国社会主义改革开放和现代化建设进程中具有标志意义的一年。"
    "在中国共产党的领导下，全国各族人民团结奋斗，国民经济继续保持较快的发展势头，"
    "经济结构的战略性调整顺利部署实施。西部大开发取得良好开端。精神文明建设和民主法制建设进一步加强。"
    "我们在过去几年取得成绩的基础上，胜利完成了第九个五年计划。我国已进入了全面建设小康社会，"
    "加快社会主义现代化建设的新的发展阶段。"
)

# 主函数
if __name__ == "__main__":
    # 构建字典
    dictionary = build_dictionary()

    # 去除标点符号（简单处理）
    import re
    test_data = re.sub(r'[^\w\s]', '', test_data)

    # 执行分词
    segmented_result = forward_maximum_matching(test_data, dictionary)

    # 输出分词结果
    print("分词结果：")
    print("/".join(segmented_result))

    # 签名
    print("\n数据225-陈俊霖-202212904506")