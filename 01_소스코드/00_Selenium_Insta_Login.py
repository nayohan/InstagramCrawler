from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import random

# 기본 정보
driver = wd.Chrome(executable_path="./chromedriver.exe")
driver.get('https://www.instagram.com/')
driver.implicitly_wait(3)
usr = ""
pwd = ""

# 로그인
driver.find_element_by_name("username").send_keys(usr)
elem = driver.find_element_by_name("password")
elem.send_keys(pwd)
elem.submit()

# 건너뛰기
driver.implicitly_wait(5)
driver.find_element_by_xpath('//button[text()="나중에 하기"]').click()
driver.implicitly_wait(3)
driver.find_element_by_xpath('//button[text()="나중에 하기"]').click()

# 검색
driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys("#맛집")      # 검색창
driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]').click() # 검색1번

# 게시글 클릭
driver.implicitly_wait(3)
driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]').click()

#Crawling #오른쪽 버튼
for i in range(0, 36000):
    print(i)
    #driver.implicitly_wait(3)
    time.sleep(random.uniform(3, 5))
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article').send_keys(Keys.ARROW_RIGHT)

    # BeatifulSoup
    html = driver.page_source
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')
    #res = soup.find_all('div', {"class": "C4VMK"})
    #res1 = soup.find_all('a', {"class": "sqdOP.yWX7d._8A5w5.ZIAjV"})
    #print(res.text)
    #for wrapper in res1:
    #    print(res1.text)
    #print(soup.select(".C4VMK")[0].text)
    #for wrapper in soup.select("a"):
    #    print(wrapper.text)

    for wrapper in soup.select("div"):
        print(wrapper.text)

