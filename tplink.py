import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import urllib.parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import schedule
import codecs
import random
import datetime
import dataset
import time
import traceback
import sys
import random
import socket
import requests
db = dataset.connect('mysql://choozmo:pAssw0rd@db.ptt.cx:3306/seo?charset=utf8mb4')
table=db['general_log']


driver = None
headers = {
        "Authorization": "Bearer " + "6SDULL1Ebklduc6TFxa97AFto5Sj21kyJ30CxiLiSoi",
        "Content-Type": "application/x-www-form-urlencoded"
}

def scrolling(driver,pgnum):
    ub = driver.find_element_by_css_selector('body')
    for i in range(pgnum):
        ub.send_keys(Keys.PAGE_DOWN)
        if pgnum>1:
            time.sleep(0.3)


def rua():
    pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125",
    ]
    return random.choice(pool)


def send_msg(kw):
    hname=socket.gethostname()
    params = {"message": hname+": "+kw}
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    

def empty_query(q):
    global driver
    googleurl='https://www.google.com/search?q='+urllib.parse.quote(q)
    driver.get(googleurl)
    time.sleep(3)


def process_query(qs):
    global driver
#    googleurl = 'https://www.google.com/search?q={}&num={}&hl={}'.format(urllib.parse.quote(q), 100,'zh-TW')
    googleurl = 'http://192.168.1.1/'

    print(googleurl)
    driver.get(googleurl)
    time.sleep(6)
#    time.sleep(9999)id="pc-login-password"
    try:
        elmt = driver.find_element(By.XPATH, "//input[@id='pc-login-password']")
        elmt.send_keys('admin')
        time.sleep(3)
        elmt = driver.find_element(By.XPATH, "//button[@id='pc-login-btn']")
        elmt.click()
        time.sleep(5)

    except:
        print('exception')

    try:
        elmt = driver.find_element(By.XPATH, "//button[@id='confirm-yes']")
        elmt.click()
    except:
        print('exception')
    time.sleep(7)
    try:
        elmt = driver.find_element(By.XPATH, "//a[@id='topReboot']")
        elmt.click()
    except:
        print('exception')
    time.sleep(2)

    try:
        elmt = driver.find_element(By.XPATH, "//button[@class='button-buttonlarge green pure-button btn-msg btn-msg-ok btn-confirm']")
        elmt.click()
    except:
        print('exception')

    time.sleep(150)
    os.system('netsh wlan connect TP-Link_78E0')
    return "ok"


def run_once():
    global driver
    result=[]
    user_agent = rua()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")
    print('before init')
    driver = webdriver.Chrome(options=options)
    print('after init')

    driver.delete_all_cookies()
    driver.set_window_size(1400,1000)
#    driver.set_window_size(900, 3000)
    print('......')
    data=process_query('')
    if data is not None:
        time.sleep(3)
    driver.quit()


os.system('netsh wlan connect TP-Link_78E0')
time.sleep(20)
run_once()