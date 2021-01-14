import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import os
import datetime

from urllib.request import urlopen, Request
import urllib
import urllib.request

url = "https://www.pinterest.co.kr"

options = webdriver.ChromeOptions()
#options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)

# 로그인 버튼 누르기 (Xpath 사용)
elem = driver.find_element_by_xpath("//*[@id='__PWS_ROOT__']/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button/div").click()
time.sleep(3)
# 로그인 정보 입력 후 로그인 하기
driver.find_element_by_id("email").send_keys("qjflsid@naver.com")
driver.find_element_by_id("password").send_keys("qjflsid")
time.sleep(5)
elem = driver.find_element_by_xpath("//*[@id='__PWS_ROOT__']/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/form/div[5]/button/div").click()
time.sleep(5)

# 나의 정보로 들어가기
elem = driver.find_element_by_xpath("//*[@id='HeaderContent']/div/div/div/div[2]/div/div/div/div[5]/div[4]/div/a").click()
time.sleep(5)

# 첫번째 보드 들어가기 (순서상)
elem = driver.find_element_by_xpath("//*[@id='__PWS_ROOT__']/div[1]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div/a").click()


interval = 5 # 5초에 한번씩 스크롤 내림

#현재 문서 높이를 가져와서 저장
prev_height = driver.execute_script("return document.body.scrollHeight")

base_path = 'C:\\Users\\Kim Juhyoung\\Desktop\\personal project'

idx = 1
os.mkdir("test")
os.chdir(base_path+"\\"+"test")
order = 1

# 반복 수행
while True:
    # 스크롤을 가장 아래로 내림
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # 페이지 로딩 대기
    driver.implicitly_wait(interval)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
    driver.implicitly_wait(interval)

    # 페이지를 soup로 바꾸고 다운로드 시작
    soup = BeautifulSoup(driver.page_source, "lxml")

    images = soup.find_all("div", attrs={"class":"XiG zI7 iyn Hsu"})

    img_srcs = [i.get('srcset') for i in soup.find_all('img', srcset=True)]

    count = 0

    for img_src in img_srcs:
        #img_src = img_src.split(" ")[6]
        len_img_src = img_src.split(" ")
        if len(len_img_src) == 8:
            img_src = len_img_src[6]
        
        elif len(len_img_src) == 6:
            img_src = len_img_src[4]
        
        elif len(len_img_src) == 4:
            img_src = len_img_src[2]
        
        else:
            img_src = len_img_src[0]

        if img_src.startswith("/originals/"):
            img_src = "https://i.pinimg.com" + img_src
        
        
        image_res = requests.get(img_src)
        image_res.raise_for_status()

        with open("pin_{}.jpg".format(idx), "wb") as f:
            f.write(image_res.content)
            idx+=1
            count += 1

    #date = f'{datetime.datetime.now():%Y-%m-%d %H:%M}'

    with open("log.txt", "at", encoding="utf8") as h:
        h.write(f"{order}. 다운받은 사진의 총 수 : {idx-1}, 다운받은 사진의 수 : {count}, 현재 페이지 높이 : {prev_height}, 시간정보 : {datetime.datetime.now():%H:%M}\n")
        h.close()
    
    order += 1

    time.sleep(interval)

    #현재 문서 높이를 가져와서 저장
    curr_height = driver.execute_script("return document.body.scrollHeight")
    if curr_height == prev_height:
        break
    else:
        prev_height = curr_height



print("스크롤 완료")

with open("log.txt", "at", encoding="utf8") as f:
    f.write("끝")

driver.quit()

 



    


#images = soup.find_all("div", attrs={"class":"XiG zI7 iyn Hsu"})

#img_srcs = [i.get('srcset') for i in soup.find_all('img', srcset=True)]


#for img_src in img_srcs:
    #img_src = img_src.split(" ")[6]
                
    #image_res = requests.get(img_src)
    #image_res.raise_for_status()
    #print(img_src)




#soup = BeautifulSoup(driver.page_source, "lxml")

#images = soup.find_all("div", attrs={"class":"XiG zI7 iyn Hsu"})


#img_srcs = [i.get('srcset') for i in soup.find_all('img', srcset=True)]
#for idx, img_src in enumerate(img_srcs):
#    img_src = img_src.split(" ")[6]
#    
#    image_res = requests.get(img_src)
#    image_res.raise_for_status()

#    with open("pin_{}".format(idx+1), "wb") as f:
#        f.write(image_res.content)
    
# XiG zI7 iyn Hsu

# https://i.pinimg.com/originals/41/4e/79/414e79d15e9e7ca23ba66fd2447355df.jpg 4x
