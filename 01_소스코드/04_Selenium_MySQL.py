from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import random
import pymysql

# 기본 정보
driver = wd.Chrome(executable_path="./chromedriver.exe")
driver.get('https://www.instagram.com/explore/tags/맛집추천/')

# 게시글 클릭
driver.implicitly_wait(3)
driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]').click()

# 인스타 로그인
usr = ""
pwd = ""
driver.find_element_by_name("username").send_keys(usr)
elem = driver.find_element_by_name("password")
elem.send_keys(pwd)
elem.submit()

# 건너뛰기
driver.implicitly_wait(3)
driver.find_element_by_xpath('//button[text()="나중에 하기"]').click()

# 게시글 클릭
driver.implicitly_wait(3)
driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]').click()

# db 로그인
hashtag_db = pymysql.connect(
    user='',
    passwd='',
    host='nuda.iptime.org',
    db='HASHTAG',
    charset='utf8mb4'
)
cur = hashtag_db.cursor(pymysql.cursors.DictCursor)

# Crawling
for i in range(0, 36000):
    print(i)
    time.sleep(random.uniform(2.5, 4.5))
    prev = time.time()
    # 크롤링
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 아이디
    id = []
    for wrapper in soup.select("a.sqdOP.yWX7d._8A5w5.ZIAjV"):
        id = wrapper.text
    id = str(id).strip('[]')
    print('아이디: ', id)
    # 장소
    location = []
    for wrapper in soup.select("a.O4GlU"):
        location = wrapper.text
    location = str(location).strip('[]')
    print('장소: ', location)
    # 날짜
    date = []
    for wrapper in soup.select("time.FH9sR.Nzb55"):
        date = wrapper['datetime'][:-5]
        break
    date = str(date).strip('[]').replace("T", " ")
    print('날짜: ', date)

    # 게시글에 있는 해시태그들
    hash_list = []
    for wrapper in soup.find_all("a", "xil3i"):
        hash_list.append(wrapper.text)
    hashtag = str(hash_list).strip('[]').replace("'", "").replace("#", "")
    print('해시태그: ', hashtag)

    # 게시글 # 해시태그 버림 # 댓글 분리
    text = []
    for tag in soup.select("div.C4VMK > span"):
        xil3i = tag.select('a.xil3i')
        for extract_tag in xil3i:
            extract_tag.extract()
        text.append(tag.getText().strip())
    if text:
        post = text[0]
        del text[0]
    else:
        post = ""
    text = str(text).strip('['']').replace("'", "")
    print('글: ', post)
    print('댓글: ', text)

    # 오른쪽 버튼
    #driver.find_element_by_xpath('/html/body/div[4]/div[2]').send_keys(Keys.ARROW_RIGHT)
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]').click()   # 글 안나올때있어서 변경

    # db 추가
    if not date:
        continue
    cur.execute("replace into HashTag (id, location, date, hashtag, post, comment) values (%s, %s, %s, %s, %s, %s)", (id, location, date, hashtag, post, text))
    hashtag_db.commit()

    print(time.time()-prev)
# db 닫기
hashtag_db.close()
