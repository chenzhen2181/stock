#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
import pandas as pd
import MySQLdb
import datetime as dt
import os

# 打开数据库连接
MYSQL_HOST = os.environ.get('MYSQL_HOST') if (os.environ.get('MYSQL_HOST') != None) else "mysqldb"
MYSQL_USER = os.environ.get('MYSQL_USER') if (os.environ.get('MYSQL_USER') != None) else "root"
MYSQL_PWD = os.environ.get('MYSQL_PWD') if (os.environ.get('MYSQL_PWD') != None) else "mysqldb"
MYSQL_DB = os.environ.get('MYSQL_DB') if (os.environ.get('MYSQL_DB') != None) else "stock_data"

local_now = dt.datetime.now()  #获取当前时间
guess_daily_filename = str(local_now.strftime("%Y_%m%d")) #以时间作为文件名，格式2023_0203

sql_1 = "SELECT `code` ,`name` FROM stock_data.stock_sina_lhb_ggtj;"   # sql语句，读取代码、名称从stock_data数据库的stock_sina_lhb_ggtj表中 (可更换guess_indicators_lite_sell_daily)
try:
    MYSQL_CONN_URL = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + ":3306/" + MYSQL_DB + "?charset=utf8mb4" 
    engine = create_engine(MYSQL_CONN_URL)  #建立engine 连接数据库
    data = pd.read_sql(sql=sql_1, con=engine)
    # data = pd.DataFrame(engine.connect().execute(text(sql_1)))   #转为pd.DataFrame数据结构，
     #  出现'OptionEngine' object has no attribute 'execute'错误 ，主要是padavan 和  sqlalchemy不再支持execute ，应该使用data = pd.DataFrame(engine.connect().execute(text(sql_1))) 
    data.to_csv("/data/logs/" + guess_daily_filename + '.txt',columns=['code'],index=0,header=0) #输出到txt (dockeer 里面路径"/data/logs/" + guess_daily_filename + '.txt')
    print (data)
except Exception as e:
    print("error :", e)
# 定时启动该文件，在docker容器中的./jobs/run_init.sh中添加nohup bash /data/stock/jobs/cron.daily/run_daily & 行后添加   /usr/local/bin/python3 /data/stock/jobs/output_data_stockdocker.py  >> /data/logs/output.log



