from flask import Flask, render_template
from flaskext.mysql import MySQL
from rediscluster import RedisCluster
import json
from flask_paginate import Pagination
from flask_paginate import get_page_args


app = Flask(__name__)

# MySQL 配置
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'dataDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

# Redis 集群配置
startup_nodes = [
    {"host": "192.168.221.101", "port": "8001"},
    {"host": "192.168.221.102", "port": "8002"},
    {"host": "192.168.221.103", "port": "8003"},
    {"host": "192.168.221.104", "port": "8004"},
    {"host": "192.168.221.105", "port": "8005"},
    {"host": "192.168.221.106", "port": "8006"}
]
redis_client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# 设置缓存过期时间
CACHE_TTL = 60000


# def get_data_from_cache_or_db(cache_key, query, table_name):
#     """
#     从 Redis 缓存中获取数据，如果缓存中没有则从 MySQL 查询并更新缓存。
#
#     :param cache_key: Redis 缓存键
#     :param query: SQL 查询语句
#     :param table_name: 表名，用于渲染模板
#     :return: 查询结果
#     """
#     # 尝试从 Redis 中获取数据
#     cached_data = redis_client.get(cache_key)
#
#     if cached_data:
#         # 如果 Redis 中有数据，直接返回
#         data = json.loads(cached_data)
#         return data
#     else:
#         # 如果 Redis 中没有数据，从 MySQL 中查询
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute(query)
#         data = cursor.fetchall()
#         cursor.close()
#         conn.close()
#
#         if data:
#             # 如果 MySQL 中有数据，更新 Redis 缓存并返回
#             redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))
#             return data
#         else:
#             return []
#

def get_data_from_cache_or_db(cache_key, query, table_name, params=None):
    """
    从 Redis 缓存中获取数据，如果缓存中没有则从 MySQL 查询并更新缓存。

    :param cache_key: Redis 缓存键
    :param query: SQL 查询语句
    :param table_name: 表名，用于渲染模板
    :param params: 查询参数（如LIMIT和OFFSET的值）
    :return: 查询结果
    """
    # 尝试从 Redis 中获取数据
    cached_data = redis_client.get(cache_key)

    if cached_data:
        # 如果 Redis 中有数据，直接返回
        data = json.loads(cached_data)
        return data
    else:
        # 如果 Redis 中没有数据，从 MySQL 中查询
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)  # 传递查询参数
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if data:
            # 如果 MySQL 中有数据，更新 Redis 缓存并返回
            redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))
            return data
        else:
            return []

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/地区')
def a():
    PER_PAGE = 10  # 每页显示的数据条目数
    page, per_page, offset = get_page_args(page_parameter='page',
                                          per_page_parameter='per_page',
                                          per_page=PER_PAGE)

    # 获取总记录数
    total_records = get_total_records('table_19')

    # 构建SQL查询语句，包含LIMIT和OFFSET子句
    query = "SELECT * FROM table_19 LIMIT %s OFFSET %s"
    cache_key = f'cache:table_19:{page}:{per_page}'

    # 使用新的缓存键从 Redis 缓存中获取数据或从 MySQL 查询
    data = get_data_from_cache_or_db(cache_key, query, 'table_12', params=(per_page, offset))

    # 创建分页对象
    pagination = Pagination(page=page, per_page=per_page, total=total_records, css_framework='bootstrap4')

    return render_template('地区.html',
                           data=data,
                           pagination=pagination)


@app.route('/症状')
def b():
    PER_PAGE = 10  # 每页显示的数据条目数
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # 获取总记录数
    total_records = get_total_records('table_10')

    # 构建SQL查询语句，包含LIMIT和OFFSET子句
    query = "SELECT * FROM table_10 LIMIT %s OFFSET %s"
    cache_key = f'cache:table_10:{page}:{per_page}'

    # 使用新的缓存键从 Redis 缓存中获取数据或从 MySQL 查询
    data = get_data_from_cache_or_db(cache_key, query, 'table_10', params=(per_page, offset))

    # 创建分页对象
    pagination = Pagination(page=page, per_page=per_page, total=total_records, css_framework='bootstrap4')

    return render_template('症状.html',
                           data=data,
                           pagination=pagination)

@app.route('/疑似职业病')
def c():
    PER_PAGE = 10  # 每页显示的数据条目数
    page, per_page, offset = get_page_args(page_parameter='page',
                                          per_page_parameter='per_page',
                                          per_page=PER_PAGE)

    # 获取总记录数
    total_records = get_total_records('table_14')

    # 构建SQL查询语句，包含LIMIT和OFFSET子句
    query = "SELECT * FROM table_14 LIMIT %s OFFSET %s"
    cache_key = f'cache:table_14:{page}:{per_page}'

    # 使用新的缓存键从 Redis 缓存中获取数据或从 MySQL 查询
    data = get_data_from_cache_or_db(cache_key, query, 'table_13', params=(per_page, offset))

    # 创建分页对象
    pagination = Pagination(page=page, per_page=per_page, total=total_records, css_framework='bootstrap4')

    return render_template('疑似职业病.html',
                           data=data,
                           pagination=pagination)

@app.route('/职业禁忌症')
def d():
    PER_PAGE = 10  # 每页显示的数据条目数
    page, per_page, offset = get_page_args(page_parameter='page',
                                          per_page_parameter='per_page',
                                          per_page=PER_PAGE)

    # 获取总记录数
    total_records = get_total_records('table_13')

    # 构建SQL查询语句，包含LIMIT和OFFSET子句
    query = "SELECT * FROM table_13 LIMIT %s OFFSET %s"
    cache_key = f'cache:table_13:{page}:{per_page}'

    # 使用新的缓存键从 Redis 缓存中获取数据或从 MySQL 查询
    data = get_data_from_cache_or_db(cache_key, query, 'table_14', params=(per_page, offset))

    # 创建分页对象
    pagination = Pagination(page=page, per_page=per_page, total=total_records, css_framework='bootstrap4')

    return render_template('职业禁忌症.html',
                           data=data,
                           pagination=pagination)

@app.route('/危害因素编码')
def e():
    PER_PAGE = 10  # 每页显示的数据条目数
    page, per_page, offset = get_page_args(page_parameter='page',
                                          per_page_parameter='per_page',
                                          per_page=PER_PAGE)

    # 获取总记录数
    total_records = get_total_records('table_12')

    # 构建SQL查询语句，包含LIMIT和OFFSET子句
    query = "SELECT * FROM table_12 LIMIT %s OFFSET %s"
    cache_key = f'cache:table_12:{page}:{per_page}'

    # 使用新的缓存键从 Redis 缓存中获取数据或从 MySQL 查询
    data = get_data_from_cache_or_db(cache_key, query, 'table_19', params=(per_page, offset))

    # 创建分页对象
    pagination = Pagination(page=page, per_page=per_page, total=total_records, css_framework='bootstrap4')

    return render_template('危害因素编码.html',
                           data=data,
                           pagination=pagination)



def get_total_records(table_name): # 获取总记录数用于完善分页显示功能
    """
    获取指定表的总记录数。

    :param table_name: 表名
    :return: 总记录数
    """
    query = f"SELECT COUNT(*) FROM {table_name}"

    # 使用 Redis 缓存来存储总记录数，以减少对数据库的压力
    cache_key = f'cache:total_records:{table_name}'
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return int(cached_data)
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        total_records = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        redis_client.setex(cache_key, 60000, total_records)

        return total_records









if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)