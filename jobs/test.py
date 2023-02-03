#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('/workspaces/stock')

from sqlalchemy import create_engine ,text
import pandas as pd
import pymysql
import MySQLdb
# 打开数据库连接
MYSQL_HOST = "localhost" #### 使用MySQLdb模块时host改为127.0.0.1；PyMySQL没有此类问题，host=localhost
MYSQL_USER = "root"
MYSQL_PWD =  "mysqldb"
MYSQL_DB = "stock_data"

# db = MySQLdb.connect("127.0.0.1", "root", "mysqldb", "stock_data", charset='utf8' )
# cursor = db.cursor()
sql_1 = "SELECT `code` FROM stock_data.stock_sina_lhb_ggtj;" 
MYSQL_CONN_URL = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + "127.0.0.1" + ":3306/" + MYSQL_DB + "?charset=utf8mb4"
engine = create_engine(MYSQL_CONN_URL)

data = pd.DataFrame(engine.connect().execute(text(sql_1)))

print (data)
# 使用 execute()  方法执行 SQL 查询 
##cursor.execute("SELECT VERSION()")
 
# 使用 fetchone() 方法获取单条数据.
data = data.drop_duplicates(subset="code", keep="last")
print("######## stat_all_lite_buy len data ########:", len(data))
 
# 关闭数据库连接
# db.close()