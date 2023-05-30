import json
import os
import scrapy
import requests
from bs4 import BeautifulSoup
from parsel import Selector
import re
from service.scraper.base_scraper import Scraper
from urllib.parse import urlparse
import uuid
from model import models
from main import db
class EbayScraper(Scraper):
    def __init__(self,url):
        super().__init__(url)
        self.header= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}

    def check_num_url(self,user_id):
        num= len( models.CrawlData.query.filter(models.CrawlData.user_id.__eq__(user_id)).all())

    
    
    
    def add_url_db(self,user_id,price_expected):
        scraper=models.CrawlData(id=str(uuid.uuid4()),url=self.url,status='Active'
                             ,price_expected=price_expected,user_id=user_id)
        db.session.add(scraper)
        db.session.commit()
        self.scraper_id=scraper.id
        return 'Success'
    
    def get_info_product_detail(self):
        headers =self.header
        r=requests.get(self.url, headers=headers)
        product={}
        soup=BeautifulSoup(r.text,'html.parser')
        main_prodcut=soup.find("div", attrs={"class": "x-price-primary"})
        img=soup.find("div", attrs={"class": "ux-image-carousel-item active image"}).find('img')
        if 'data-src' in str(img):
            product['image'] = img['data-src']
            
        else:
            product['image'] = img['src']
        product['url']=self.url
        parsed_url = urlparse(self.url)
        product['short_url'] = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        name=soup.select_one('h1.x-item-title__mainTitle > span').text
        product['name'] = name
        price = soup.select_one('div.x-price-primary > span > span.ux-textspans').text
        number = re.findall(r'\d+\.\d+', price)
        product['price'] = number[0]
        return product
    
        


