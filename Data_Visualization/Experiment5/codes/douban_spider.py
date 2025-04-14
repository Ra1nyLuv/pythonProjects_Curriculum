import requests
from bs4 import BeautifulSoup
import time
import jieba
from pyecharts import options as opts
from pyecharts.charts import WordCloud as PyWordCloud
import os

from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = 'https://cdn.bootcdn.net/ajax/libs/echarts/5.4.2/'
current_dir = os.path.dirname(os.path.abspath(__file__))


MOVIE_ID = '1296339'
BASE_URL = f'https://movie.douban.com/subject/{MOVIE_ID}/comments'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_comments():
    comments = []
    urls = [f'{BASE_URL}?start={i*20}&limit=20&status=P&sort=new_score' for i in range(5)]
    
    for url in urls:
        try:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('span', class_='short')
            comments.extend([item.text.strip() for item in items])
            time.sleep(1)
        except Exception as e:
            print(f'Error fetching {url}: {str(e)}')
    
    with open(os.path.join(current_dir, 'douban_comments.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(comments))
    return comments


def generate_wordcloud(text):
    words = jieba.lcut(text)

    
    stopwords = ['，', '。', ' ', '：', '「', '」', '、']
    
    word_counts = {}
    for word in words:
        if word not in stopwords and len(word) > 1:
            word_counts[word] = word_counts.get(word, 0) + 1
    
    word_counts = {k:v for k,v in word_counts.items() if v >= 2}
    
    print(f'有效词汇数量: {len(word_counts)}')
    if word_counts:
        top10 = sorted(word_counts.items(), key=lambda x: -x[1])[:10]
        print(f'高频词汇TOP10: {top10}')
    
    wc = (
        PyWordCloud()
        .add(series_name="影评词云",
             data_pair=sorted(word_counts.items(), key=lambda x: x[1], reverse=True),
             word_size_range=[20, 100],
             shape='diamond', 
             rotate_step=45)  
        .set_global_opts(title_opts=opts.TitleOpts(title="豆瓣影评词云"),
                        toolbox_opts=opts.ToolboxOpts())
    )
    from wordcloud import WordCloud as MatWordCloud
    import matplotlib.pyplot as plt
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    wc = MatWordCloud(
        font_path='simhei.ttf',
        width=800,
        height=600,
        background_color='white',
        max_words=200
    ).generate_from_frequencies(word_counts)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(os.path.join(current_dir, 'douban_wordcloud.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # pyecharts词云生成（保留原有功能）
    py_wc = (PyWordCloud()
        .add(series_name="影评词云",
             data_pair=sorted(word_counts.items(), key=lambda x: x[1], reverse=True),
             word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="豆瓣影评词云"))
    )
    py_wc.render(os.path.join(current_dir, "douban_wordcloud.html"))
    return word_counts

if __name__ == '__main__':
    all_comments = fetch_comments()
    
    print(f"清洗前词汇数量: {len(jieba.lcut(' '.join(all_comments)))}")
    word_counts = generate_wordcloud(' '.join(all_comments))
    
    with open(os.path.join(current_dir, 'douban_comments.txt'), 'r', encoding='utf-8') as f:
        sample_text = f.read(500)
    print(f"清洗后高频词汇示例: {sorted(word_counts.items(), key=lambda x: -x[1])[:10]}")