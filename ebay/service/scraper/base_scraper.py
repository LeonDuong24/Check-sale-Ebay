import uuid
from main import db
from model import models

class Scraper():
    def __init__(self,url):
        super().__init__()
        self.url=url
        self.id_db=None
    
    def add_url_db(self):
        try:
            scraper=models.CrawlData(id=str(uuid.uuid4()),url=self.url,status='active')
            db.session.add(scraper)
            db.session.commit()
            self.id_db=scraper.id
            return True
        except Exception as e:
            print(e)
            return False    
    
    def content_mail(self,product):
        html = f"""\
        <html>
        <body>
        <h1>The product {product['name']} sale</h1>
        <img src="{product['image']}">
        <h2>Price now sale {product['price']} at:  {product['short_url']}</h2>
        </body>
        </html>
        """
        return html
    

