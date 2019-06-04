import time
import urllib
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service

from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MailQuery(Base):
    __tablename__ = 'MailQuery'
    id = Column(Integer, primary_key=True)
    number = Column(String(20))
    html = Column(Text)
    query_type = Column(Integer)
    route_json = Column(Text)

engine = create_engine('mysql+pymysql://root:mrtTest1234@plus@172.24.100.84:3306/mrt')
DBSession = sessionmaker(bind=engine)

session = DBSession()
querys = session.query(MailQuery).all()
browser = webdriver.Firefox(executable_path='D:\download\geckodriver.exe')
for query in querys:
    # load the page and input number
    browser.get("https://www.royalmail.com/track-your-item#/")
    WebDriverWait(browser, 20, 0.5).until(
        EC.presence_of_all_elements_located((By.ID, 'track-item'))
    )
    input_tb = browser.find_element_by_id('track-item')
    input_tb.click()
    input_tb.send_keys(query.number)
    submit_btn = browser.find_element_by_id('trackdelivery-bt')
    submit_btn.click()

    WebDriverWait(browser, 6000, 0.5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'see-history-link'))
    )
    query.html = browser.page_source
session.commit()
session.close()
