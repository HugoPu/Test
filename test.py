# import urllib.request as urllib2
# # user_agent是爬虫与反爬虫斗争的第一步
# ua_headers = {
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'en',
#     'Origin': 'https://www.royalmail.com',
#     'Referer': 'https://www.royalmail.com/track-your-item',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
#     'X-IBM-Client-ID': 'c43cc33d-e308-415c-a848-4f60be6db45c',
#     # 'X-Recaptcha-Session': 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGljb25uZWN0IiwiYXVkIjoiVEFQSXYyIiwiZXhwIjoxNTU4MzIzODk1LCJpYXQiOjE1NTgzMjI5OTV9.H6lrUlDoyp7cIF_FGeg1ZI-6LLS4WCTFc5u6--Y8Mno',
#     'X-RMG-API-Session': 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGljb25uZWN0IiwiYXVkIjoiVEFQSXYyIiwiZXhwIjoxNTU4MzIzODk1LCJpYXQiOjE1NTgzMjI5OTV9.H6lrUlDoyp7cIF_FGeg1ZI-6LLS4WCTFc5u6--Y8Mno',
#     'X-RMG-Language': 'en_GB',
#     'X-Recaptcha-Session': 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGljb25uZWN0IiwiYXVkIjoiVEFQSXYyIiwiZXhwIjoxNTU4MzM0Nzk4LCJpYXQiOjE1NTgzMzM4OTh9.53HTkyVCZ1IhEx6K-Ol4KiAUPRQ0ppFc7qEpH6cVQjM'
# }
# # 通过Request()方法构造一个请求对象
# url = r'https://api.royalmail.net/mailpieces/v2/MN389613107GB/events'
# request = urllib2.Request(url, headers = ua_headers)
# print(request.headers,request.type,request.data)
#
# # 向指定的url地址发送请求，并返回服务器响应的类文件对象
# response = urllib2.urlopen(request)
#
# # 服务器返回的类文件对象支持python文件对象的操作方法
# html = response.read()

import time
import urllib
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service

i = 0
options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.binary = None
browser = webdriver.Firefox(executable_path='F:\Anaconda3\envs\DL\Lib\geckodriver.exe', options=options)

while True:
    browser.get("https://www.royalmail.com/track-your-item#/")

    WebDriverWait(browser, 20, 0.5).until(
        EC.presence_of_all_elements_located((By.ID, 'track-item'))
    )
    input_tb = browser.find_element_by_id('track-item')
    input_tb.click()
    input_tb.send_keys('MN389613107GB')
    submit_btn = browser.find_element_by_id('trackdelivery-bt')
    submit_btn.click()

    WebDriverWait(browser, 6000, 0.5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'see-history-link'))
    )
    if i == 0:
        start = time.clock()
    elapsed = (time.clock() - start)
    i = i + 1
    print('{}:{}:'.format(i, elapsed))

