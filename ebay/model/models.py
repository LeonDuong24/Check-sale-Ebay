from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Import root directory
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, Text,Boolean,BigInteger
from sqlalchemy.orm import relationship
from main import db, app
from service import mail
from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy import func
import uuid
# class UserMixin(object):
#     @declared_attr
#     def user_update(cls):
#         return db.Column(db.String(50), nullable=False, default=current_user.name)

class Base(db.Model):
    __abstract__=True
    id = Column(String(255), primary_key=True,index=True)
    update_date= Column(DateTime,default=func.now(), onupdate=func.now() )
    note = Column(String(100))

class CrawlData(Base):
    __tablename__ = 'Crawl_data'
    url = Column(Text, nullable=False)
    short_url = Column(Text, nullable=False)
    status = Column(String(50),index=True)
    num_wrong = Column(Integer, default=0)
    num_check= Column(Integer, default=0)
    #prev_time_check=Column(DateTime)
    created_on= Column(DateTime)
    time_next_check= Column(DateTime)
    price_expected=Column(Integer)
    int_time_next_check= Column(BigInteger,index=True)
    user = relationship('User', backref='Crawl_data', lazy=True)
    user_id=Column(String(255), ForeignKey('User.id'), nullable=False,index=True)

class User_type(Base):
    __tablename__ = 'User_type'
    #id = Column(String(255), primary_key=True)
    user_role = Column(String(20))  
    max_num_check=Column(Integer)
    min_num_check=Column(Integer)
    time_check=Column(Float)


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = Column(String(255), primary_key=True)
    user_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    user_type_id=Column(String(255), ForeignKey('User_type.id'), nullable=False)
    user_type = relationship('User_type', backref='User', lazy=True)
    #user_role = Column(String(20), default='USER')
    img = Column(Text)
    def __str__(self):
        return self.user_name
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()