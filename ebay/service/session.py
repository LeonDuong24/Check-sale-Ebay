import uuid
from service.scraper.ebay_scraper import EbayScraper
from service.mail import Mail
from model import models
from main import db
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.decorate import retry


def get_url_with_user(user_id):
    return models.CrawlData.query.filter(models.CrawlData.user_id.__eq__(user_id)).all()

#@retry(max_attempts=3,retry_interval=10)
def add_url(url,price_expected,user_id):
    scraper=models.CrawlData(id=str(uuid.uuid4()),url=url,status='Active'
                             ,price_expected=price_expected,user_id=user_id)
    db.session.add(scraper)
    db.session.commit()
    return 'Success',scraper.id

#@retry(max_attempts=5,retry_interval=10)
def check_price(url_id):
    crawler=models.CrawlData.query.get(url_id)
    ebay=EbayScraper(crawler.url)
    product=ebay.get_info_product_detail()
    if float(product['price']) < float(crawler.price_expected):
        crawler.status='Done'
        db.session.commit()
        html=ebay.content_mail(product)
        Mail(subject='Ebay sale',html=html,receiver_email=crawler.user.email).send()
        del ebay
        return True 
    # if crawler.num_wrong > 5:
    #     crawler.status='Pending'
    #     return
    # crawler.num_wrong+=1
    # db.session.commit()
    # return False