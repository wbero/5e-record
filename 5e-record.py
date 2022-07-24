import requests
import re
import html2text
from bs4 import BeautifulSoup
import js2xml
import numpy as np
from hoshino import Service, priv
from hoshino.typing import CQEvent, MessageSegment as ms

sv = Service('_5e_', manage_priv=priv.SUPERUSER, visible=False)
@sv.on_prefix('5e查询')
async def arena_miner(bot, ev: CQEvent):
      try:
            userid = ev.message.extract_plain_text()

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
            htmlurl = f'https://arena.5eplay.com/api/search/player/1/16?keywords={userid}'

            r = requests.get(htmlurl, headers=headers)
            html = r.text
            name = re.findall('"domain":".*?"', html)
            user_name = (name[0].split('"')[-2])    # 获取真实id

            htmlurl2 = f'https://arena.5eplay.com/data/player/{user_name}'# 主页
            #print(htmlurl2)
            r2 = requests.get(htmlurl2, headers=headers)
            html2 = r2.text

            soup= BeautifulSoup(html2, 'html.parser')
            data = soup.text
            #print(data)
            #overall_ranking = re.findall('总排名', data)
            overall_number = re.findall('\d+', str(re.findall('总比赛\n\d', data)))[0]
            rws = re.findall('(\d+(\.\d+)?)', str(re.findall('贡献值RWS\n[\d+\.\d+]*', data)[0]))[0][0]

            rating = re.findall('(\d+(\.\d+)?)', str(re.findall('技术得分Rating\n[\d+\.\d+]*', data)[0]))[0][0]
            high_ladder = re.findall('\d+', str(re.findall('天梯\n\d+', data)))[0]
            all_time = re.findall('\d+', str(re.findall('游戏时长\n\d+', data)))[0]
            kills_number = re.findall('(\d+(\.\d+)?)', str(re.findall('平均每局杀敌\n[\d+\.\d+]*', data)[0]))[0][0]
            # print(str(re.findall('平均每局杀敌\n[\d+\.\d+]*', data)[0]))
            kills_assists = re.findall('(\d+(\.\d+)?)', str(re.findall('平均每局助攻\n[\d+\.\d+]*', data)[0]))[0][0]
            # print(str(re.findall('平均每局助攻\n[\d+\.\d+]*', data)[0]))
            alive = re.findall('(\d+(\.\d+)?)', str(re.findall('每局存活率\n[\d+\.\d+]*', data)[0]))[0][0]
            mvp = re.findall('\d+', str(re.findall('MVP\n\d+', data)))[0]
            KD = re.findall('(\d+(\.\d+)?)', str(re.findall('K/D\n[\d+\.\d+]*', data)[0]))[0][0]
            rifleman = re.findall('(\d+(\.\d+)?)', str(re.findall('爆头率\n[\d+\.\d+]*', data)[0]))[0][0]
            odds = re.findall('\d+', str(re.findall('胜率\n\d+', data)))[0]

            msg = f'{userid}的总比赛数为{overall_number},\nRWS为{rws},\nRating为{rating},\n天梯分数为{high_ladder},\n游戏时长为{all_time}h,\n平均每局杀敌为{kills_number},\n平均每局助攻为{kills_assists},\n每局存活率为{alive},\nMVP次数为{mvp},\nK/D为{KD},\n爆头率为{rifleman},\n胜率为{odds}%'
            await bot.send(ev,msg)
      except:
            bug=f"数据出错，请检查昵称是否拼错"
            await bot.send(ev,bug)








