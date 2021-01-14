# -*- coding:utf-8 -*- 

import discord, asyncio

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

from urllib.request import urlopen, Request
import urllib
import urllib.request


def create_soup(url):
    hdr = {"User-Agent":"[user agent string]"}
    res = requests.get(url, headers=hdr)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


token = "[discord bot token]"
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("반갑습니다 :D"))
    print("I'm Ready!")
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.content == ("!명령어"):
        embed = discord.Embed(title= "명령어 모음", description="", color=0x62c1cc)
        embed.add_field(name="!날씨", value="[살고 있는 동네 이름]동의 날씨를 알려줌", inline=False)
        embed.add_field(name="오늘의 뉴스", value="오늘의 헤드라인 뉴스 3개를 알려줌", inline=False)
        embed.add_field(name="IT뉴스", value="IT뉴스 3개를 알려줌", inline=False)
        embed.add_field(name="!주식", value="!주식 뒤에 오는 회사의 주식정보를 알려줌", inline=False)
        embed.add_field(name="!롤", value="!롤 뒤에 오는 소환사의 전적정보를 알려줌", inline=False)
        embed.add_field(name="!롤_인게임", value="!롤_인게임 뒤에 오는 소환사의 인게임 정보를 알려줌", inline=False)
        await message.channel.send(embed=embed) # 메시지가 보내진 채널에 메시지를 보내는 방식

    
    if message.content == ("!날씨"):
        url = "[자신이 살고있는 동네의 날씨 정보를 가진 naver 날씨 url]"
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
        embed = discord.Embed(title="오늘의 날씨")
        embed.add_field(name="종합날씨", value=cast, inline=False)
        embed.add_field(name="온도", value=f"현재 {curr_temp} (최저 {min_temp} / 최고 {max_temp})", inline=False)
        embed.add_field(name="강수확률", value=f"오전 {rain_rate_morning} / 오후 {rain_rate_afternoon}", inline=False)
        embed.add_field(name="미세먼지", value= pm10, inline=False)
        embed.add_field(name="초미세먼지", value=pm25, inline=False)
        await message.channel.send(embed=embed)

    
    if message.content == "!오늘의 뉴스":
        url = "https://news.naver.com"
        soup = create_soup(url)
        # 뉴스리스트 생성 (3개)
        news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3)
        # 출력
        embed = discord.Embed(title="헤드라인 뉴스")
        for index, news in enumerate(news_list):
            title = news.find("a").get_text().strip()
            link = url + news.find("a")["href"]
            embed.add_field(name=str(index+1) + "." + title, value=link, inline=False)
        await message.channel.send(embed=embed)


    if message.content == "!IT뉴스":
        url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
        soup = create_soup(url)
        # 뉴스 리스트 생성 (3개)
        news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3)
        # 출력
        embed = discord.Embed(title="IT뉴스")
        for index, news in enumerate(news_list):
            a_idx = 0
            img = news.find("img")
            if img:
                a_idx = 1 # img 태그가 있으면 1번째 a 태그의 정보를 사용
            a_tag = news.find_all("a")[a_idx]
            title = a_tag.get_text().strip()
            link = a_tag["href"]
            embed.add_field(name=str(index+1) + "." + title, value=link, inline=False)
        await message.channel.send(embed=embed)


    if message.content.startswith("!롤_인게임"):
        learn = message.content.split(" ") # 분리
        location = learn[1:] # !롤을 제외한 나머지 (소환사의 이름)
        for i in range(len(location)):
            if i == 0:
                name = location[i]
            else:
                name = name + "+" + location[i]
        
        url = "https://www.op.gg/summoner/userName=" + name
        driver = webdriver.Chrome()
        driver.get(url)
        elem = driver.find_element_by_link_text("인게임 정보").click()
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        link = soup.find("link").attrs['href']

        ingame_info = soup.find("div", attrs={"class":"tabItem Content SummonerLayoutContent summonerLayout-spectator"})

        embed = discord.Embed(title="롤_인게임 정보")
        embed.add_field(name="Team", value="Blue", inline=False)

        ingame_name_blues = soup.find("table", attrs={"class":"Table Team-100"}).find("tbody").find_all("td", attrs={"id":"live_summoner"})
        ingame_tier_blues = soup.find("table", attrs={"class":"Table Team-100"}).find("tbody").find_all("div", attrs={"class":'TierRank'})

        for i in range(0,5):
            embed.add_field(name="소환사의 이름: " + ingame_name_blues[i].get_text().strip(), 
            value="티어: " + ingame_tier_blues[i].get_text().strip(), inline=False)

        
        await message.channel.send(embed=embed)


client.run(token)