import datetime
import time
import pandas as pd
import pymysql 
from utils import date_time
from service.session import check_price
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app,config_name,ZONE
with app.app_context():
#     SQL_URL=f'mysql://root:1234@localhost:3306/WebSale'
#     engine = create_engine(SQL_URL)
#     time_now_int=date_time.change_time_to_int(str(date_time.get_time_now_with_zone('America/New_York')),'%Y-%m-%d %H:%M:%S')
#     query = f"""select * from crawl_data
#                 where status="Active" and int_time_next_check <= {time_now_int}
#                 limit 10
#                     """
#     df = pd.read_sql_query(query,engine)
#     if df.size!=0:
#         for index,i in df.iterrows():
#             print(check_price(i['id']))
#     else:
#         print("Nothing found")
#         query = f"""select min(int_time_next_check) from crawl_data
#                 where status="Active"
#                     """
#         df = pd.read_sql_query(query,engine)
#         time_next_check =df['min(int_time_next_check)'].values- time_now_int-200
#         time.sleep(time_next_check[0])
    print(check_price('30447fd7-95ba-4a73-8772-ad8542f3b200'))