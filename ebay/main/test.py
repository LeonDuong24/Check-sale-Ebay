import datetime
import json
import re
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import requests 
from sqlalchemy import create_engine
import sys
import os
url='https://www.ebay.com/itm/383459556814'
r=requests.get(url)
product={}
soup=BeautifulSoup(r.text,'html.parser')
main_prodcut=soup.find("div", attrs={"class": "x-price-primary"})
img=soup.find("div", attrs={"class": "ux-image-carousel-item active image"}).find('img')
if 'data-src' in str(img):
    product['image'] = img['data-src']
    
else:
    product['image'] = img['src']
product['url']=url
parsed_url = urlparse(url)
product['short_url'] = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
name=soup.select_one('h1.x-item-title__mainTitle > span').text
product['name'] = name

#price = soup.select_one('div.vim-buybox-wrapper > div.vim x-buybox > div.x-buybox__section > div.x-buybox__price-section > div.vim x-bin-price > div.x-bin-price__content > div.x-price-primary > span > span.ux-textspans').text
price=soup.select_one('.x-price-primary .ux-textspans').text
number = re.findall(r'\d+\.\d+', price)
product['price'] = number[0]
print(product)


