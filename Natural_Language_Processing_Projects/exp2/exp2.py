import os
import re
import jieba
from collections import defaultdict
import math
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

if not os.path.exists("news_articles"):
    os.makedirs("news_articles")

def crawl_news_articles(base_url, num_articles=50):
    articles = []
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        print("页面部分内容预览：", soup.prettify()[:1000])

        links = []
        for item in soup.find_all('a', href=True):
            href = item['href']
            if "163.com" in href and href.endswith(".html") and ("/article/" in href or "/dy/" in href):
                links.append(href)

        unique_links = list(set(links))[:num_articles]
        print(f"找到 {len(unique_links)} 个有效链接：", unique_links[:5])  

        for link in unique_links:
            article = fetch_article_content(link)
            if article:
                articles.append(article)
                save_article_to_file(article)

    except Exception as e:
        print(f"爬取错误：{e}")

    return articles

def fetch_article_content(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 调整标题和正文的选择器
        title_tag = soup.find("h1")  
        if not title_tag:
            return None
        title = title_tag.get_text().strip()

        content = []
        for p in soup.find_all("p"):  
            text = p.get_text().strip()
            if text and len(text) > 20: 
                content.append(text)
        content = "\n".join(content)

        return {"title": title, "content": content, "url": url}

    except Exception as e:
        print(f"提取文章失败：{url}，错误：{e}")
        return None


def save_article_to_file(article):
    file_name = re.sub(r'[\\/*?:"<>|]', "", article["title"])[:50] + ".txt"
    file_path = os.path.join("news_articles", file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"标题: {article['title']}\n")
        f.write(f"链接: {article['url']}\n\n")
        f.write("正文:\n")
        f.write(article["content"])

    print(f"已保存文章: {file_name}")

# 数据清洗
def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# 分词函数
def tokenize(text):
    words = jieba.lcut(text)
    return [word for word in words if len(word) > 1]  # 过滤单字

# 计算逆文档频率 (IDF)
def calculate_idf(docs):
    idf_dict = defaultdict(int)
    total_docs = len(docs)

    # 统计每个词出现在多少篇文档中
    for doc in docs:
        unique_words = set(tokenize(clean_text(doc)))
        for word in unique_words:
            idf_dict[word] += 1

    # 计算 IDF 值
    for word, count in idf_dict.items():
        idf_dict[word] = math.log(total_docs / (count + 1))

    return idf_dict

# 计算词频 (TF)
def calculate_tf(doc):
    words = tokenize(clean_text(doc))
    tf_dict = defaultdict(int)
    total_words = len(words)

    for word in words:
        tf_dict[word] += 1

    for word in tf_dict:
        tf_dict[word] /= total_words

    return tf_dict

# 计算 TF-IDF 并提取前 N 个关键字
def extract_keywords(doc, idf_dict, top_n=5):
    tf_dict = calculate_tf(doc)
    tfidf_scores = {}

    for word, tf in tf_dict.items():
        if word in idf_dict:
            tfidf_scores[word] = tf * idf_dict[word]

    # 按照 TF-IDF 值排序，提取前 N 个关键字
    sorted_keywords = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [word for word, score in sorted_keywords]

# 主函数
if __name__ == "__main__":
    # 爬取网易科技频道的文章
    base_url = "https://tech.163.com/"
    articles = crawl_news_articles(base_url, num_articles=50)

    # 加载所有文章内容
    cleaned_docs = []
    for file_name in os.listdir("news_articles"):
        file_path = os.path.join("news_articles", file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            cleaned_docs.append(content)

    # 计算 IDF
    idf_dict = calculate_idf(cleaned_docs)

    # 选择一篇文档进行测试
    test_doc = cleaned_docs[0] if cleaned_docs else ""

    # 提取关键字
    keywords = extract_keywords(test_doc, idf_dict, top_n=5)

    # 输出结果
    print("测试文档：")
    print(test_doc[:100])  # 只打印前100个字符
    print("\n提取的前5个关键字：")
    print(keywords)

    # 签名
    print("\n数据225-陈俊霖-202219204506")

