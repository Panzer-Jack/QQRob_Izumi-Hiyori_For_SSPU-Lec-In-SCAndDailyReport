import pymysql

# 你的数据库和表名
db = ""
db_table = ""

# 连接 你的MYSQL数据库
# 注：这里默认是使用本地数据库接口，若你使用的是云服务器的话可以自行配置 Host 成你的云数据库服务器的IP
def mysql_QQ_rootFind():
    """机器人 使用权限查询"""
    SSPU_DB = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='xxxxxx',
        database=db,
        charset='utf8'
    )
    cur = SSPU_DB.cursor()
    sql = f'select * from {db_table}'
    cur.execute(sql)
    res = cur.fetchall()
    SSPU_DB.close()
    return res


def mysql_QQ_rootAdd(QQ_num_T, type):

    return 0
