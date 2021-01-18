# -*- coding:utf-8 -*- 

import discord, asyncio

import requests
from bs4 import BeautifulSoup

import time
import re

from urllib.request import urlopen, Request
import urllib
import urllib.request

token = "<토큰 정보>"
client = discord.Client()


def create_soup(url):
    hdr = {"User-Agent":"<user agent 정보>",
    'Accept-Language':"ko-KR"}
    res = requests.get(url, headers=hdr)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def lol_user_name_plus(learn):
    location = learn[1:]
    for i in range(len(location)):
        if i == 0:
            name = location[i]
        else:
            name = name + "+" + location[i]
    return name

def lol_user_name(learn):
    location = learn[1:]
    for i in range(len(location)):
        if i == 0:
            name = location[i]
        else:
            name = name + " " + location[i]
    return name
        

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
        embed.add_field(name="!날씨", value="부곡동의 날씨를 알려줌", inline=False)
        embed.add_field(name="오늘의 뉴스", value="오늘의 헤드라인 뉴스 3개를 알려줌", inline=True)
        embed.add_field(name="경제뉴스", value="경제뉴스 3개를 알려줌", inline=False)
        embed.add_field(name="it뉴스", value="it뉴스 3개를 알려줌", inline=False)
        embed.add_field(name="오늘의 회화", value="해커스 영어 회화를 알려줌", inline=False)
        embed.add_field(name="!롤", value="!롤 뒤에 오는 소환사의 전적정보를 알려줌", inline=False)
        embed.add_field(name="!인게임-롤", value="!인게임-롤 뒤에 오는 소환사의 인게임 정보를 알려줌", inline=False)
        embed.add_field(name="!최근게임-롤", value="!최근게임-롤 뒤에 오는 소환사의 최근게임 정보를 알려줌", inline=False)
        await message.channel.send(embed=embed) # 메시지가 보내진 채널에 메시지를 보내는 방식

    
    if message.content == ("!날씨"):
        url = "<자신이 사는 동네의 네이버 날씨 정보 url>"
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
        embed = discord.Embed(title="오늘의 날씨", color=0xA9F5F2)
        embed.add_field(name="종합날씨", value=cast, inline=False)
        embed.add_field(name="온도", value=f"현재 {curr_temp} (최저 {min_temp} / 최고 {max_temp})", inline=False)
        embed.add_field(name="강수확률", value=f"오전 {rain_rate_morning} / 오후 {rain_rate_afternoon}", inline=False)
        embed.add_field(name="미세먼지", value= pm10, inline=False)
        embed.add_field(name="초미세먼지", value=pm25, inline=False)
        await message.channel.send(embed=embed)

    
    if message.content == "!오늘의 뉴스":
        url = "https://news.naver.com/"
        soup = create_soup(url)
        # 뉴스리스트 생성 (5개)
        news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=5)
        # 출력
        embed = discord.Embed(title="헤드라인 뉴스", color=0xD358F7)
        for index, news in enumerate(news_list):
            title = news.find("a").get_text().strip()
            link = url + news.find("a")["href"]
            embed.add_field(name=str(index+1) + "." + title, value=link, inline=False)
        await message.channel.send(embed=embed)


    if message.content == "!경제뉴스":
        url = "https://news.naver.com"
        soup = create_soup(url)
        # 뉴스리스트 생성 (5개)
        news_list = soup.find("div",{"id":"section_economy"}).find("ul", attrs={"class":"mlist2 no_bg"}).find_all("li", limit=5)
        # 출력
        embed = discord.Embed(title="경제뉴스", color=0xADFF2F)
        for index, news in enumerate(news_list):
            title = news.find("a").get_text().strip()
            link = url + news.find("a")["href"]
            embed.add_field(name=str(index+1) + "." + title, value=link, inline=False)
        await message.channel.send(embed=embed)


    if message.content == "!it뉴스":
        url = "https://news.naver.com"
        soup = create_soup(url)
        # 뉴스리스트 생성 (5개)
        news_list = soup.find("div",{"id":"section_it"}).find("ul", attrs={"class":"mlist2 no_bg"}).find_all("li", limit=5)
        # 출력
        embed = discord.Embed(title="it뉴스", color=0x0404B4)
        for index, news in enumerate(news_list):
            title = news.find("a").get_text().strip()
            link = url + news.find("a")["href"]
            embed.add_field(name=str(index+1) + "." + title, value=link, inline=False)
        await message.channel.send(embed=embed)


    if message.content == "!오늘의 회화":
        url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english#;"
        soup = create_soup(url)
        sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})

        embed = discord.Embed(title="오늘의 영어 회화", description="하루에 하나!", color=0xACFA58)

        embed.add_field(name="영어지문", value="English", inline=False)

        for sentence in sentences[len(sentences)//2:]: # 8문장이 있다고 가정할 때, 5~8 까지 잘라서 가져옴 (인덱스 기준 : 4~7)
            sentence = sentence.get_text().strip().split(":")
            embed.add_field(name=sentence[0],value=sentence[1], inline=False)
        
        embed.add_field(name="-"*20, value="-"*20,inline=False)
        
        embed.add_field(name="한글지문", value="korean", inline=False)

        for sentence in sentences[:len(sentences)//2]: # 8문장이 있다고 가정할 때, 1~4 까지 잘라서 가져옴 (인덱스 기준 : 0~3)
            sentence = sentence.get_text().strip().split(":")
            embed.add_field(name=sentence[0],value=sentence[1], inline=False)

        await message.channel.send(embed=embed)


    if message.content.startswith("!롤"):
        learn = message.content.split(" ") # 분리
        name = lol_user_name_plus(learn)
        url = "https://www.op.gg/summoner/userName=" + name
        soup = create_soup(url)
        name = lol_user_name(learn)

        player_level = soup.find("div", {"class":"Header"}).find("div",{"class":"ProfileIcon"}).find("span").get_text().strip()
        ladderLank = soup.find("div", {"class":"Header"}).find("div",{"class":"LadderRank"})
        
        if ladderLank == None:
            ladderLank = "순위없음"
            embed = discord.Embed(title=name, description="소환사레벨: " + player_level + "\n" + 
            "래더 랭킹: " + ladderLank, color=0x848484)

        else:
            ladderLank = soup.find("div", {"class":"Header"}).find("div",{"class":"LadderRank"}).find("span").get_text().strip()
            top_rate = soup.find("div", {"class":"Header"}).find("div",{"class":"LadderRank"}).get_text().strip()
            top_rate = top_rate.split(" ")
            top_rates = top_rate[3:]
            for i in range(len(top_rates)):
                if i == 0:
                    top_rate = top_rates[i]
                else:
                    top_rate = top_rate + " " + top_rates[i]
            embed = discord.Embed(title=name, description="소환사레벨: " + player_level + "\n" + 
            "래더 랭킹: " + ladderLank + "위 " + top_rate , color=0x848484)


        Thumbnail = soup.find("div", {"class":"Header"}).find("div",{"class":"ProfileIcon"}).find("img")["src"]
        Thumbnail = "https:" + Thumbnail

        image_medal = soup.find("div", {"class":"SideContent"}).find("img", {"class":"Image"})["src"]
        image_medal = "https:" + image_medal

        embed.set_thumbnail(url= Thumbnail)

        embed.set_author(name="OP.GG 전적검색", url=url, icon_url=image_medal)


        # 티어 정보를 출력한다. (없다면 unranked를 출력한다.)
        tier_rank_info = soup.find("div", attrs={"class": "SideContent"}).find("div", attrs={"class":"TierRankInfo"})
        lank_type = tier_rank_info.find("div", attrs={"class":"RankType"}).get_text().strip()

        if tier_rank_info.find("div", {"class":"TierRank unranked"}) != None:
            tier_rank = "Unranked"
            embed.add_field(name=lank_type, value=tier_rank, inline=False)
        else:
            tier_rank = tier_rank_info.find("div", attrs={"class":"TierRank"}).get_text().strip()
            current_LP = tier_rank_info.find("div", attrs={"class":"TierInfo"}).find("span", attrs={"class":"LeaguePoints"}).get_text().strip()
            WinLose = tier_rank_info.find("div", {"class":"TierInfo"}).find("span",{"class":"WinLose"})
            wins = WinLose.find("span", {"class":"wins"}).get_text().strip()
            Loses = WinLose.find("span", {"class":"losses"}).get_text().strip()
            winratio = WinLose.find("span", {"class":"winratio"}).get_text().strip()
            if tier_rank_info.find("div", attrs={"class":"LeagueName"}) == None:
                embed.add_field(name=lank_type, value=tier_rank + current_LP + " - " + "\n" + wins + " / " + Loses + " (" + winratio + ")", inline=False)
            else:
                league_name = tier_rank_info.find("div", attrs={"class":"LeagueName"}).get_text().strip()
                embed.add_field(name=lank_type, value=tier_rank + current_LP + " - " + league_name + "\n" + wins + " / " + Loses + " (" + winratio + ")", inline=False)


        # 최근 20게임에 대한 전적을 알려준다.
        current_game = soup.find("div", {"class":"Content"}).find("table", {"class":"GameAverageStats"})
        Total = current_game.find("td", {"class":"Title"})
        total_game = Total.find("span", {"class":"total"}).get_text().strip() + "전 "
        win = Total.find("span", {"class":"win"}).get_text().strip() + "승 "
        lose = Total.find("span", {"class":"lose"}).get_text().strip() + "패 "

        KDA = current_game.find("td", {"class":"KDA"}).find("div", {"class":"KDA"})
        Kill = KDA.find("span", {"class":"Kill"}).get_text().strip() + " /"
        Death = KDA.find("span", {"class":"Death"}).get_text().strip() + " /"
        Assist = KDA.find("span", {"class":"Assist"}).get_text().strip()

        KDA_Ratio = current_game.find("td", {"class":"KDA"}).find("div", {"class":"KDARatio"})
        KDARatio = KDA_Ratio.find("span",{"class":"KDARatio"}).get_text().strip()
        KDApercent = KDA_Ratio.find("span", {"class":"CKRate tip"}).find("span").get_text().strip()

        embed.add_field(name="최근게임", value=total_game + win + lose + "\n" +
        Kill + Death + Assist + "\n" +
        KDARatio + " (" + KDApercent + ")", inline=False)

        # 모스트 챔피언 테이블 가져오기 (없다면 없다고 출력)
        most_champs = soup.find("div", {"class":"SideContent"}).find("div", {"class":"MostChampionContent"})

        if most_champs != None:
            most_champs = soup.find("div", {"class":"SideContent"}).find("div", {"class":"MostChampionContent"}).find_all("div", {"class":"ChampionBox Ranked"})
        
            champs = ""
            cs_rates = ""
            win_ratop_playeds = ""

            for most_champ in most_champs:
                champ = most_champ.find("div", {"class":"ChampionName"}).get_text().strip()
                cs = most_champ.find("div", {"class":"ChampionMinionKill tip"}).get_text().strip()
                rate = most_champ.find("span",{"class":"KDA"}).get_text().strip()
                win_ratio = most_champ.find("div", {"title":"승률"}).get_text().strip()
                played = most_champ.find("div", {"class":"Title"}).get_text().strip()

                champs = champs + champ + "\n"
                cs_rates = cs_rates + cs + " " + rate + "\n"
                win_ratop_playeds = win_ratop_playeds + "승률: " + win_ratio + " (" + played + ")" + "\n"

            embed.add_field(name="모스트챔피언", value= "`" + champs + "`", inline=True)
            embed.add_field(name="CS/평점", value= "`" + cs_rates + "`", inline=True)
            embed.add_field(name="전적", value= "`" + win_ratop_playeds + "`", inline=True)
        else:
            embed.add_field(name="모스트챔피언", value="정보가 없습니다. ㅠㅅㅠ", inline=False)

        await message.channel.send(embed=embed)


    if message.content.startswith("!인게임-롤"):
        learn = message.content.split(" ") # 분리
        name = lol_user_name_plus(learn)
        url = "https://www.op.gg/summoner/spectator/userName=" + name
        soup = create_soup(url)

        embed = discord.Embed(title="Team Blue", description="파랑이 좋겠군", color=0x0054FF)
        #embed.add_field(name="Team", value="Blue", inline=False)

        ingame_name_blues = soup.find("table", attrs={"class":"Table Team-100"}).find("tbody").find_all("td", attrs={"id":"live_summoner"})
        ingame_tier_blues = soup.find("table", attrs={"class":"Table Team-100"}).find("tbody").find_all("div", attrs={"class":'TierRank'})

        for i in range(0,5):
            embed.add_field(name="소환사의 이름: " + ingame_name_blues[i].get_text().strip(), 
            value="티어: " + ingame_tier_blues[i].get_text().strip(), inline=False)
        
        await message.channel.send(embed=embed)

        embed = discord.Embed(title="Team Red", description="빨간색이 3배 더 강하겠군", color=0xFF0000)
        #embed.add_field(name="Team", value="Red", inline=False)

        ingame_name_reds = soup.find("table", attrs={"class":"Table Team-200"}).find("tbody").find_all("td", attrs={"id":"live_summoner"})
        ingame_tier_reds = soup.find("table", attrs={"class":"Table Team-200"}).find("tbody").find_all("div", attrs={"class":'TierRank'})
        
        for i in range(0,5):
            embed.add_field(name="소환사의 이름: " + ingame_name_reds[i].get_text().strip(), 
            value="티어: " + ingame_tier_reds[i].get_text().strip(), inline=False)

        await message.channel.send(embed=embed)


    if message.content.startswith("!최근게임-롤"):
        learn = message.content.split(" ") # 분리
        name = lol_user_name_plus(learn)
        url = "https://www.op.gg/summoner/userName=" + name
        soup = create_soup(url)
        
        name = lol_user_name(learn)

        Recent_games = soup.find("div", {"class":"GameItemList"}).find("div", {"class":"Content"})

        game_type = Recent_games.find("div",{"class":"GameType"}).get_text().strip() 
        game_result = Recent_games.find("div",{"class":"GameResult"}).get_text().strip() 
        game_length = Recent_games.find("div",{"class":"GameLength"}).get_text().strip() 

        game_setting = Recent_games.find("div",{"class":"GameSettingInfo"})
        champ_img_url = game_setting.find("div",{"class":"ChampionImage"}).find("img")["src"] 
        champ_img_url = "https:" + champ_img_url 
        champ_name = game_setting.find("div",{"class":"ChampionName"}).get_text().strip() 

        game_Kill = Recent_games.find("div",{"class":"KDA"}).find("span",{"class":"Kill"}).get_text().strip()
        game_Death = Recent_games.find("div",{"class":"KDA"}).find("span",{"class":"Death"}).get_text().strip()
        game_Assist = Recent_games.find("div",{"class":"KDA"}).find("span",{"class":"Assist"}).get_text().strip()
        game_KDA_Ratio = Recent_games.find("div",{"class":"KDA"}).find("span",{"class":"KDARatio"}).get_text().strip()

        game_stat = Recent_games.find("div",{"class":"Stats"})
        game_level = game_stat.find("div",{"class":"Level"}).get_text().strip()
        game_CS = game_stat.find("div",{"class":"CS"}).find("span").get_text().strip()
        game_Kill_rate = game_stat.find("div",{"class":"CKRate tip"}).get_text().strip()

        game_levels = game_level.split(" ")
        game_level = game_levels[-1]

        game_Kill_rates = game_Kill_rate.split(" ")
        game_Kill_rate = game_Kill_rates[-1]

        game_items = Recent_games.find("div",{"class":"ItemList"}).find_all("div",{"class":"Item"})

        accessories = ""

        if game_items[3].find("div", {"class":"Image NoItem"}) == None:
            accessories = "장신구 : `" + game_items[3].find("img")["alt"] + "`"
        else:
            accessories = "왜 장신구가 없죠?"

        game_items_name = ""

        for idx, game_item in enumerate(game_items):
            if game_item.find("div", {"class":"Image NoItem"}) == None:
                if game_item.find("img")["alt"] == game_items[3].find("img")["alt"]:
                    game_items_name = game_items_name + "\n"
                    continue
                game_item_names = game_item.find("img")["alt"]
                game_items_name = game_items_name + "`" + game_item_names + "`" + " , "
            
        game_items_name = game_items_name + "\n" + accessories           
        
        # 아직은 미완성 같은 느낌임
        # 장신구를 기준으로 아이템창을 나누어서 \n처리를 하였으나
        # 좀더 완성도 있게 하려면 위에서 no_item인 경우와 장신구인 경우를 미리 거르고
        # item안에 있는 것들로 //연산자와 len()을 이용하여 가운데로 나누어서 2줄 배치하는 것이 보다 보기 좋다.

               
        embed = discord.Embed(title=champ_name + " - " + game_type + " (" + game_result + ")",
        description= "KDA: " + game_Kill + " / " + game_Death + " / " + game_Assist + " (" + game_KDA_Ratio + ")" + "\n"
        + "Level: " + game_level + "\n"
        + "CS: " + game_CS + "\n"
        + "킬 관여: " + game_Kill_rate + "\n"
        + "게임시간: " + game_length + "\n"
        ,color=0x088A68)

        embed.set_thumbnail(url = champ_img_url)
        embed.set_author(name=name + "의 최근게임")
        
        embed.add_field(name="최종아이템", value=game_items_name, inline=False)


        await message.channel.send(embed=embed)


client.run(token)