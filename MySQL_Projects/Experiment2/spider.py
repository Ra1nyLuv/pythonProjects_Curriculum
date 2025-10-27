import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector

# 设置请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


# 函数：从豆瓣电影Top250页面获取电影信息
def get_movie_info(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = []

    for item in soup.select('.item'):
        rank = item.find('em').get_text()
        title = item.find('span', class_='title').get_text()
        rating = item.find('span', class_='rating_num').get_text()
        link = item.find('a')['href']
        movie_list.append([rank, title, rating, link])

    return movie_list


# 主函数
def main():
    base_url = 'https://movie.douban.com/top250'
    all_movies = []

    # 分页爬取所有电影信息
    for i in range(0, 250, 25):
        url = f'{base_url}?start={i}&filter='
        movies = get_movie_info(url)
        all_movies.extend(movies)

    # 显示部分结果
    print("部分电影信息预览:")
    for movie in all_movies[:5]:  # 打印前5条记录
        print(f"{movie[0]} {movie[1]} {movie[2]} {movie[3]}")

    # 将结果保存到CSV文件
    df = pd.DataFrame(all_movies, columns=['排名', '中文片名', '评分', '链接'])
    df.to_csv('/tmp/movies.csv', index=False, encoding='utf-8-sig')
    print("电影信息已成功保存至movies.csv")

    # 将结果保存到MySQL数据库
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',  # 替换为你的实际密码
            database='douban',
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        # 创建表时指定字符集
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rank INT,
                title VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                rating FLOAT,
                link VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            )
        ''')

        # 插入数据到MySQL
        for movie in all_movies:
            cursor.execute('INSERT INTO movies (rank, title, rating, link) VALUES (%s, %s, %s, %s)',
                           (int(movie[0]), movie[1], float(movie[2]), movie[3]))

        conn.commit()
        cursor.close()
        conn.close()
        print("电影信息已成功保存至MySQL数据库")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


if __name__ == '__main__':
    main()