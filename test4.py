import time
import pyautogui

from pyautogui import tweens
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BUSTER_COLOR = (255, 178, 105)# The orange color of recaptcha buster
IMAGE_MODE_BUSTER_BUTTON = (557, 887)

BOT_WARNING_BUTTON_COLOR = (74, 144, 226)
BOT_WARNING_BUTTON_POS = (530, 540)

VIDOE_MODE_DOWNLOAD_COLOR = (112, 112, 112)
VIDOE_MODE_DOWNLOAD_BUTTON = (835, 740)
VIDEO_MODE_BUSTER_BUTTON = (820, 795)
VIDEO_MODE_REFRESH_BUTTON = (723, 800)

def get_querys():
    # TODO
    class Query(object):
        pass
    query = Query()
    query.number = 'MN389613107GB'
    return [query]

def generate_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument(r'--user-data-dir=C:\Users\hugo\AppData\Local\Google\Chrome\User Data')
    options.add_argument((r'--profile-directory=Profile 2'))
    options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    browser = webdriver.Chrome(executable_path='D:\download\chromedriver.exe', chrome_options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1280, 960)
    return browser

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
    else:
        return False
    pyautogui.moveTo(IMAGE_MODE_BUSTER_BUTTON, duration=0.3, tween=tweens.easeInOutBounce)
    pyautogui.click()
    time.sleep(1)

    if per_time_check_pixel_color(0.5, 0.5, BOT_WARNING_BUTTON_COLOR, BOT_WARNING_BUTTON_POS):
        # TODO: Write log
        return False

    while(per_time_check_pixel_color(0, 0, VIDOE_MODE_DOWNLOAD_COLOR, VIDOE_MODE_DOWNLOAD_BUTTON)):
        # time.sleep(12)
        # check_video_mode = pyautogui.pixelMatchesColor(*VIDEO_MODE_BUSTER_BUTTON, BUSTER_COLOR, tolerance=15)
        if per_time_check_pixel_color(0.5, 0.5, BUSTER_COLOR, VIDEO_MODE_BUSTER_BUTTON):
            # pyautogui.moveTo(VIDEO_MODE_REFRESH_BUTTON, duration=0.5, tween=tweens.easeInOutBounce)
            # pyautogui.click()
            pyautogui.moveTo(VIDEO_MODE_BUSTER_BUTTON, duration=0.5, tween=tweens.easeInOutBounce)
            pyautogui.click()

            pyautogui.moveTo(IMAGE_MODE_BUSTER_BUTTON, duration=0.1)

    return True

def access_mail_info_page(browser, number):
    try:
        browser.get("https://www.royalmail.com/track-your-item#/")
        WebDriverWait(browser, 20, 0.5).until(
            EC.presence_of_all_elements_located((By.ID, 'track-item'))
        )
        input_tb = browser.find_element_by_id('track-item')
        input_tb.click()
        input_tb.send_keys(number)
        submit_btn = browser.find_element_by_id('trackdelivery-bt')
        submit_btn.click()
    except TimeoutException as e:
        print()
        # ToDo Write log

    try:
        WebDriverWait(browser, 5, 1).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'see-history-link'))
        )
    except TimeoutException as e:
        if check_captcha():
            x, y = browser.get_window_position()
            submit_btn = browser.find_element_by_id('trackdelivery-bt')
            submit_btn.click()
        else:
            # TODO: Write log
            raise Exception

    return browser


def query_mail():
    querys = get_querys()
    browser = generate_browser()
    for query in querys:
        temp_browser = access_mail_info_page(browser, query.number)
        query.html = temp_browser.page_source
        # TODO: write recod to db
    browser.quit()

query_mail()




