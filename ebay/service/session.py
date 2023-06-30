import datetime
import json
import threading
import time
import traceback
import uuid
from service import mysql
from service.scraper.ebay_scraper import EbayScraper
from service.mail import Mail
from model import models
from main import db
from main.config import config_by_name
from utils import date_time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.decorate import retry
from urllib.parse import urlparse
from main import app,CONFIG,ZONE,logger
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine,text,desc
def get_all_users():
    return models.User.query.all()

def get_url_with_user(user_id):
    return models.CrawlData.query.filter(models.CrawlData.user_id.__eq__(user_id)).order_by(desc(models.CrawlData.created_on)).all()

def get_all_url():
    return models.CrawlData.query.filter().all()

def delet_url_with_id(id):
    try:
        engine = create_engine(CONFIG.SQL_URL)
        query = f"""DELETE  
                    from Crawl_data
                    where id= "{id}"
                        """
        flag=mysql.excute_query(query,engine)
        return True
    except:
        logger.error(traceback.format_exc())
        return False

def count_url():
    try:
        engine = create_engine(CONFIG.SQL_URL)
        query = f"""Select count(*)  
                    from Crawl_data
                        """
        with engine.connect() as connection:
            result=connection.execute(text(query))
            row_count = result.scalar()
        return row_count
    except:
        logger.error(traceback.format_exc())
        return 151

@retry(max_attempts=3,retry_interval=10)
def add_url(url,price_expected,user_id,option,name_product):
    parsed_url = urlparse(url)
    if option:
        option=option.strip()
        # input_dict = dict(item.strip().split(':') for item in option.split('/'))
        # option = ','.join([f'"{key}":"{value}"' for key, value in input_dict.items()])
    print(option)
    user:models.User
    user=(models.User.query.get(user_id))
    hour=user.user_type.time_check
    time_now=date_time.get_time_now_with_zone(ZONE)
    time_int=date_time.change_time_to_int(str(date_time.get_time_now_with_zone(ZONE)+datetime.timedelta(hours=hour)),'%Y-%m-%d %H:%M:%S')
    short_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    scraper=models.CrawlData(id=str(uuid.uuid4()),url=url,short_url=short_url
                             ,status='Active'
                             ,created_on=time_now,update_date=time_now,int_time_next_check=time_int,time_next_check=time_now+datetime.timedelta(hours=hour)
                             ,price_expected=price_expected,user_id=user_id,note=option,name_product=name_product) #
    db.session.add(scraper)
    db.session.commit()
    return 'Success',scraper.id

@retry(max_attempts=5,retry_interval=10)
def get_infor_product(ebay:EbayScraper):
    product=ebay.get_info_product_detail()
    return product

def update_time(crawler:models.CrawlData):
    time_now=date_time.get_time_now_with_zone(ZONE)
    hour=crawler.user.user_type.time_check
    time_int=date_time.change_time_to_int(str(date_time.get_time_now_with_zone(ZONE)+datetime.timedelta(hours=hour)),'%Y-%m-%d %H:%M:%S')
    crawler.time_next_check=time_now+datetime.timedelta(hours=hour)
    crawler.int_time_next_check=time_int
    crawler.update_date=time_now
    return crawler

def check_price(url_id):
    with app.app_context():
        try:
            print(url_id)
            crawler:models.CrawlData
            crawler=models.CrawlData.query.get(url_id)
            ebay=EbayScraper(crawler.url,url_id)
            product=get_infor_product(ebay)
            if float(product['price']) <= float(crawler.price_expected):
                crawler.status='Done'
                db.session.commit()
                html=ebay.content_mail(product)
                Mail(subject='Ebay sale',html=html,receiver_email=crawler.user.email).send()
                del ebay
                return True
            else:
                crawler.num_check+=1
                crawler=update_time(crawler)
                time_now=date_time.get_time_now_with_zone(ZONE)
                hour=crawler.user.user_type.time_check
                # time_int=date_time.change_time_to_int(str(date_time.get_time_now_with_zone(ZONE)+datetime.timedelta(hours=hour)),'%Y-%m-%d %H:%M:%S')
                
                # crawler.time_next_check=time_now+datetime.timedelta(hours=hour)
                # crawler.int_time_next_check=time_int
                # crawler.update_date=time_now
                db.session.commit()
                return False
        except Exception as e:
            logger.error(traceback.format_exc())
            crawler.num_wrong+=1
            crawler=update_time(crawler)
            db.session.commit() 
            # if crawler.num_wrong > 0:
            #     crawler.status='Pending'
            #     db.session.commit() 
            #     return False
            return False
