# project : 웹 스크래핑을 이용하여 나만의 비서를 만들기

# 조건
# 1. 네이버에서 오늘 현재 지역의 날씨정보를 가져온다
# 2. 헤드라인 뉴스 3건을 가져온다
# 3. IT 뉴스 3건을 가져온다
# 4. 해커스 어학원 홈페이지에서 오늘의 영어 회화 지문을 가져온다

import requests
from bs4 import BeautifulSoup


def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
    print("{}. {}".format(index+1, title))
    print("  (링크 : {})".format(link))


def scrape_weather():   # 날씨 정보 가져오기 함수
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EA%B5%B0%ED%8F%AC+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    # 날씨, 어제보다 @@
    cast = soup.find("p", attrs={"class":"cast_txt"}).get_text()
    # 현재 @@도씨 (최저@@, 최고@@)
    curr_temp = soup.find("p", attrs={"class":"info_temperature"}).get_text().replace("도씨", "") # 현재온도
    min_temp = soup.find("span", attrs={"class":"min"}).get_text() # 최저온도
    max_temp = soup.find("span", attrs={"class":"max"}).get_text() # 최고온도
    # 오전 강수확률 @@% / 오후 강수확률 @@%
    rain_rate_morning = soup.find("span", attrs={"class":"point_time morning"}).get_text().strip() # 오전강수 확률
    rain_rate_afternoon = soup.find("span", attrs={"class":"point_time afternoon"}).get_text().strip() # 오후강수 확률
    #미세먼지, 초미세먼지
    dust = soup.find("dl", attrs={"class":"indicator"})
    pm10 = dust.find_all("dd")[0].get_text() # 미세먼지
    pm25 = dust.find_all("dd")[1].get_text() # 초미세먼지

    # 출력
    print(cast)
    print("현재 {} (최저 {} / 최고{})".format(curr_temp, min_temp, max_temp))
    print("오전 {} / 오후 {}".format(rain_rate_morning, rain_rate_afternoon))
    print()
    print("미세먼지 {}".format(pm10))
    print("초미세먼지 {}".format(pm25))
    print()


def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print_news(index, title, link)
    print()


def scrape_IT_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = news.find("a")["href"]
        print_news(index, title, link)







if __name__ == "__main__":
    #scrape_weather() # 오늘의 날씨 정보 가져오기
    #scrape_headline_news()
    scrape_IT_news()