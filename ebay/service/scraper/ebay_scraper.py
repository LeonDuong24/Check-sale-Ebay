import json
import os
import time
import scrapy
import requests
from bs4 import BeautifulSoup
from parsel import Selector
import re
from service.scraper.base_scraper import Scraper
from urllib.parse import urlparse
import uuid
from model import models
from main import db,config_name
import selenium
from selenium.webdriver.support.select import Select
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
if config_name=='prod':
    chrome_options.binary_location = '/usr/bin/google-chrome'
#chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
import itertools
class EbayScraper(Scraper):
    def __init__(self,url,id=None):
        super().__init__(url)
        self.header= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        if id is not None:
            self.scraper:models.CrawlData
            self.scraper=models.CrawlData.query.filter(models.CrawlData.id.__eq__(id)).first()

    def check_num_url(self,user_id):
        num= len( models.CrawlData.query.filter(models.CrawlData.user_id.__eq__(user_id)).all())
    
    def add_url_db(self,user_id,price_expected):
        scraper=models.CrawlData(id=str(uuid.uuid4()),url=self.url,status='Active'
                             ,price_expected=price_expected,user_id=user_id)
        db.session.add(scraper)
        db.session.commit()
        self.scraper_id=scraper.id
        return 'Success'
    
    def list_select_product(self,driver):
        els = driver.find_elements('class name','x-msku__select-box')
        selects = []
        for el in els:
            # Adding the dropdown name to the select object
            name = el.get_attribute('selectboxlabel')
            select = Select(el)
            select.name = name
            selects.append(select)
        for idx, sel in enumerate(selects):
            sel.values = [option.text for option in sel.options][1:]
        return selects
    
    def all_optional_of_select_prodcut(self,selects):
        #print("Get all options for each dropdown")
        for idx, sel in enumerate(selects):
            sel.values = [option.text for option in sel.options][1:]
            print(sel.values)
        #print("Get all possible permutations")
        permutations = list(itertools.product(*[sel.values for sel in selects]))
        return permutations
    
    def list_detail_option_product(self):
        driver = Chrome(options=chrome_options)
        driver.get(self.url)
        selects=self.list_select_product(driver)
        formatted_string = '{' + self.scraper.note + '}'
        dictionary = json.loads(formatted_string)
        len_options = len(dictionary)
        li=list(value.split(',') for key, value in dictionary.items())
        permutations = list(itertools.product(*li))
        list_option=self.detail_option_product(driver,selects,permutations,len_options)
        driver.close()
        return list_option
    
    def detail_option_product(self,driver,selects,permutations,len_options):
        #print("Select all possible permutation and get price for each")
        results = []
        for permutation in permutations:
            # Resetting all parameter to default
            for sel in selects:
                try:
                    sel.select_by_index(0)
                except Exception as e:
                    pass
            # Iteration to set each dropdown
            result = self.apply_values_dropdown(selects, permutation)
            if result:
                # Once all dropdown value are set, get the finally price
                time.sleep(1)
                #price=soup.select_one('.x-price-primary .ux-textspans').text
                price=driver.find_element('xpath', '//div[@class="x-price-primary"]/span[@class="ux-textspans"]').text
                number = re.findall(r'\d+\.\d+', price)
                result['Price'] = number[0]#driver.find_element("css selector", ".x-price-primary").find_element("css selector", 'span[itemprop="price"]').get_attribute('content')#driver.find_element_by_id("prcIsum").text
                print(result['Price'])
                if len(result) == len_options +1:
                    results.append(result)
        return results
    
    def apply_values_dropdown(self,dropdowns, values):
        """
        :param dropdowns: list of select DropDown
        :param values: list of values to set
        :return: dict with key=dropdownName, value=dropDownValue
        """
        r = {}
        for value in values:
            # For each value, get the associated DropDown and set it
            for dropdown in dropdowns:
                if value in dropdown.values:
                    try:
                        dropdown.select_by_visible_text(value)
                        r[dropdown.name] = value
                    except Exception:                 
                        continue
        return r

    

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
        if self.scraper.note:
            optional_product=self.list_detail_option_product()
            min_item= min(optional_product, key=lambda x: float(x['Price']))
            product['price']=min_item['Price']
            min_item.pop('Price')
            option_str = ', '.join([f"{key}: {value}" for key, value in min_item.items()])
            product['name'] += ' '+option_str
        else:
            #price = soup.select_one('div.x-bin-price__content > div.x-price-primary > span > span.ux-textspans').text
            price=soup.select_one('.x-price-primary .ux-textspans').text
            number = re.findall(r'\d+\.\d+', price)
            product['price'] = number[0]
        return product
    


    