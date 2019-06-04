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
import pyautogui
from pyautogui import tweens
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service

BUSTER_COLOR = (248, 176, 104) # The color of recaptcha buster
IMAGE_MODE_BUSTER_BUTTON = (760, 950)

FULL_DATA_BUTTON = (274, 958)
FULL_DATA_BUTTON_COLOR = (64, 64, 64)

VIDOE_MODE_DOWNLOAD_COLOR = (112, 112, 112)
VIDOE_MODE_DOWNLOAD_BUTTON = (835, 740)
VIDEO_MODE_BUSTER_BUTTON = (820, 795)
VIDEO_MODE_REFRESH_BUTTON = (723, 800)

i = 0
options = webdriver.ChromeOptions()
# options.add_argument('disable-infobars')
options.add_argument(r'--user-data-dir=C:\Users\hugo\AppData\Local\Google\Chrome\User Data')
# options.add_argument(r'--user-data-dir=C:\Users\hugo\AppData\Local\Google\Chrome\User Data')
options.add_argument((r'--profile-directory=Profile 1'))
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
# user_agent = ('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')
options.add_argument('user-agent=%s'%user_agent)
options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

browser = webdriver.Chrome(executable_path='D:\download\chromedriver.exe', chrome_options=options)

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



def check_pixel_color(rgb, position=None, tolerance=10):
    if position is None:
        x, y = pyautogui.position()
    else:
        x, y = position

    return pyautogui.pixelMatchesColor(x, y, rgb, tolerance=tolerance)

def per_time_check_pixel_color(every_time, total_time, rgb, position=None, tolerance=10):

    sum_time = 0
    while True:
        if check_pixel_color(rgb, position, tolerance):
            return True
        if sum_time >= total_time:
            return False
        time.sleep(every_time)
        sum_time += every_time

def check_captcha():
    # image mode
    for i in range(30):
        if per_time_check_pixel_color(0.05, 0.1, BUSTER_COLOR, IMAGE_MODE_BUSTER_BUTTON):
            break
        if per_time_check_pixel_color(0.05, 0.1, FULL_DATA_BUTTON_COLOR, FULL_DATA_BUTTON):
            return True
    else:
        return False
    # check_img_mode = pyautogui.pixelMatchesColor(*IMAGE_MODE_BUSTER_BUTTON, BUSTER_COLOR, tolerance=15)
    # if not check_img_mode:
    #     return True
    pyautogui.moveTo(IMAGE_MODE_BUSTER_BUTTON, duration=1, tween=tweens.easeInOutBounce)
    pyautogui.click()
    time.sleep(1)

    while(per_time_check_pixel_color(0, 0, VIDOE_MODE_DOWNLOAD_COLOR, VIDOE_MODE_DOWNLOAD_BUTTON)):
        # time.sleep(12)
        # check_video_mode = pyautogui.pixelMatchesColor(*VIDEO_MODE_BUSTER_BUTTON, BUSTER_COLOR, tolerance=15)
        if per_time_check_pixel_color(0.5, 0.5, BUSTER_COLOR, VIDEO_MODE_BUSTER_BUTTON):
            pyautogui.moveTo(VIDEO_MODE_REFRESH_BUTTON, duration=1, tween=tweens.easeInOutBounce)
            pyautogui.click()
            pyautogui.moveTo(VIDEO_MODE_BUSTER_BUTTON, duration=1, tween=tweens.easeInOutBounce)
            pyautogui.click()

            pyautogui.moveTo(IMAGE_MODE_BUSTER_BUTTON, duration=0.1)

    return True

