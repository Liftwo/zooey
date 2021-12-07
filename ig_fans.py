import time
from requests.cookies import RequestsCookieJar
import requests
from selenium import webdriver
from headers import rua
import re
import json
import pymysql.cursors


class IgSpider():
    def __init__(self):
        self.path = "D:\DeepLearning\chromedriver.exe"
        self.sbaccount = 'tsaizooey@aol.com'
        self.sbpd = 'jondae350'

    def ig_token(self):  # 獲得登入後的cookie
        driver = webdriver.Chrome(self.path)
        driver.implicitly_wait(3)
        driver.get('https://www.instagram.com/')
        time.sleep(5)
        account = driver.find_elements_by_name('username')[0]
        pd = driver.find_elements_by_name('password')[0]
        time.sleep(5)
        account.send_keys(self.sbaccount)
        pd.send_keys(self.sbpd)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()  # 登入
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
        time.sleep(3)
        cookie = driver.get_cookies()
        jar = RequestsCookieJar()
        for i in cookie:
            jar.set(i['name'], i['value'])
        driver.close()
        return jar

    def download_fans(self, url):
        cookies = self.ig_token()
        s = requests.session()
        headers = {"User-Agent": rua(),
                   }
        connection = pymysql.connect(host='', port=10000, user='root', password='easycatchball168', db='hinh')
        cursor = connection.cursor()
        print('資料庫連結成功')
        query = "SELECT * FROM hinh.drfcreator_creatordetails  where platform='ig' order by -id limit 144;"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            time.sleep(3)
            print(row)
            url = row[9]
            try:
                res = s.get(url=url, headers=headers, cookies=cookies).text
                json_match = re.search(r'window\._sharedData = (.*);</script>', res)
                profile_json = json.loads(json_match.group(1))['entry_data']['ProfilePage'][0]['graphql']['user']
                follows = profile_json['edge_followed_by']['count']
                print(follows)
                update = f"UPDATE `hinh`.`drfcreator_creatordetails` SET `fans` = {follows}  WHERE (`id` = {row[0]});"
            except:
                print('無此頁面')
                continue
            try:
                cursor.execute(update)
                connection.commit()
            except:
                print('無法更新資料庫', url)
                continue

        connection.close()


class SaveToDb():
    connection = pymysql.connect(host='127.0.0.1', user='root', password='nicc1314', db='hinh')
    cursor = connection.cursor()
    print('資料庫連結成功')
    query = "SELECT * FROM hinh.drfcreator_creatordetails  where platform='ig' order by -id limit 144;"


    cursor.execute(query)
    result = cursor.fetchall()
    print('result',result)
    for row in result:
        url = row[8]
        print('url',url)
        follows = IgSpider().download_fans(url)
        print(follows)
        update = f"UPDATE `hinh`.`drfcreator_creatordetails` SET `fans` = {follows}  WHERE (`id` = {row[0]});"
        cursor.execute(update)
        connection.commit()

    connection.close()

if __name__ == '__main__':
    IgSpider()




