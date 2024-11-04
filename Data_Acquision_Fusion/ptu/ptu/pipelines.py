import mysql.connector

class PtuPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='192.168.221.101',
            user='root',
            password='1234',
            database='ptu',
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            "INSERT INTO menuList (menu, url) VALUES (%s, %s)",
            (item['menu'], item['url'])
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()