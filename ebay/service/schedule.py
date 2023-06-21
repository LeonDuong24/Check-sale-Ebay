import datetime
import multiprocessing
import threading
import time
import traceback
import uuid
from service.scraper.ebay_scraper import EbayScraper
from concurrent.futures.thread import ThreadPoolExecutor
from service.mail import Mail
from model import models
from main import db
from main.config import config_by_name
from utils import date_time
from service.logger import logger
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.session import check_price
from service.decorate import retry
from urllib.parse import urlparse
from main import app,CONFIG,ZONE
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine,text

def process_data(row):
    try:
        check_price(row['id'])
    except:
        pass


def schedule_check_price():
    #with app.app_context():
        num_cores = multiprocessing.cpu_count()
        while True:
            try:
                engine = create_engine(CONFIG.SQL_URL)
                time_now_int=date_time.change_time_to_int(str(date_time.get_time_now_with_zone(ZONE)),'%Y-%m-%d %H:%M:%S')
                print(time_now_int)
                query = f"""select id,status,int_time_next_check 
                            from Crawl_data
                            where status="Active" and int_time_next_check <= {time_now_int}
                            limit 10
                        """
                df = pd.read_sql_query(query,con=engine)
                if df.size!=0:
                    with ThreadPoolExecutor(max_workers=num_cores) as executor:
                        for index,row in df.iterrows():
                            executor.submit(process_data, row)
                # else:
                #     print("Nothing found")
                #     query = f"""select min(int_time_next_check) from Crawl_data
                #         where status="Active"
                #             """
                #     df = pd.read_sql_query(query,engine)
                #     if df['min(int_time_next_check)'].values[0] != None:
                #         time_next_check =df['min(int_time_next_check)'].values- time_now_int
                #         #time.sleep(time_next_check[0])
                #     else:
                #         print("Nothing")
                engine.dispose()
                time.sleep(60)
            except Exception as e:
                print(traceback.format_exc())
                logger.error(traceback.format_exc())
                time.sleep(60)