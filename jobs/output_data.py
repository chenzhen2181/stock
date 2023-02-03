#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine ,text
import pandas as pd
import MySQLdb
import datetime as dt


# 打开数据库连接
MYSQL_HOST = "127.0.0.1" #### 使用MySQLdb模块时host改为127.0.0.1；PyMySQL没有此类问题，host=localhost
MYSQL_USER = "root"
MYSQL_PWD =  "mysqldb"
MYSQL_DB = "stock_data"

local_now = dt.datetime.now()  #获取当前时间
guess_daily_filename = str(local_now.strftime("%Y_%m%d")) #以时间作为文件名，格式2023_0203

sql_1 = "SELECT `code` ,`name` FROM stock_data.stock_sina_lhb_ggtj;"   # sql语句，读取代码、名称从stock_data数据库的stock_sina_lhb_ggtj表中 (可更换guess_indicators_lite_sell_daily)
try:
    MYSQL_CONN_URL = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + ":3306/" + MYSQL_DB + "?charset=utf8mb4" 
    engine = create_engine(MYSQL_CONN_URL)  #建立engine 连接数据库
    #data = pd.read_sql(sql=sql_1, engine) 
    data = pd.DataFrame(engine.connect().execute(text(sql_1)))   #转为pd.DataFrame数据结构，
     #  出现'OptionEngine' object has no attribute 'execute'错误 ，主要是padavan 和  sqlalchemy不再支持execute ，应该使用data = pd.DataFrame(engine.connect().execute(text(sql_1))) 
    data.to_csv("/workspaces/stock/dockerindocker/.stock/data/logs/" + guess_daily_filename + '.txt',columns=['code'],index=0,header=0) #输出到txt (dockeer 里面路径"/data/logs/" + guess_daily_filename + '.txt')
    print (data)
except Exception as e:
    print("error :", e)



