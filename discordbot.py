from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(token)

# Horoscope
def uranai(text):
    response_string = ''
    seiza = 100
    date = datetime.datetime.today().strftime("%Y/%m/%d")
    index_st = text.find(' ')+1
    index_ed = text.find('座')+1
    search_text = text[index_st:index_ed]
    print(search_text)
    seiza_list = ("牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座")
    seiza_list2 = ("おひつじ座", "おうし座", "ふたご座", "かに座", "しし座", "おとめ座", "てんびん座", "さそり座", "いて座", "やぎ座", "みずがめ座", "うお座") 
    try:
        seiza = seiza_list.index(search_text)
    except:
        try:
            seiza = seiza_list2.index(search_text)
        except Exception as e:
            response_string = "君の星が…見えない… :cloud:"
    try:
        res = requests.get(url='http://api.jugemkey.jp/api/horoscope/free/'+ date)
        txt = res.json()["horoscope"][date][seiza]
        job = emoji(int(txt["job"]), "job")
        money = emoji(int(txt["money"]), "money")
        love = emoji(int(txt["love"]), "love")
        total = emoji(int(txt["total"]), "total")
        response_string = "今日の**" + txt["sign"] + "**の運勢は。。。**" + str(txt["rank"]) + "位**！\n" + txt["content"] + "\nラッキーアイテムは**" + txt["item"] + "**で、ラッキーカラーは**" + txt["color"] + "**。\n仕事運："+job+"\n金　運：" + money + "\n恋愛運：" + love + "\nトータルは..." + total + "です！良い一日を！"
        #print(response_string)
    except Exception as e:
        print("君の星が…見えない… :cloud:")
    return response_string

def emoji(number, category):
    res = ''
    for i in range(number):
        if category == 'job':
            res += ':briefcase: '
        elif category == 'money':
            res += ':moneybag: '
        elif category == 'love':
            res += ':heart: '
        elif category == 'total':
            res += ':star: '
    return res

# Omikuji
def omikuji():
    response_string = ''
    lots = ["大吉", "吉", "中吉", "小吉", "半吉", "末吉", "末小吉", "平", "凶", "小凶", "半凶", "末凶", "大凶", "未分"]
    random.shuffle(lots)
    lot = lots[0]
    print(lot)
    response_string = "あなたの運勢は...ｶﾞｼｬｶﾞｼｬｶﾞｼｬｶﾞｼｬ...\n\n　　　　" + lot + "　ですね！"

    return response_string

import discord
import wikipedia
import requests
import json
import random

client = discord.Client()
TOKEN = "ここにトークンを書いてね"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # 「雲さん」で始まるか調べる
    if message.content.startswith("1_1さん"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            try:
                user_name = message.author.name
                text = message.content
                print(text)
                print(type(text))

                ################# Don't touch. ################
                kumo_san = 1_1
                ################# Don't touch. ################

                msg =  kumo_san + user_name + 'さん '
                #msg = user_name + 'さん '

                if text == ('1_1'):
                    msg = 'はい！ご用でしょうか！'
                elif text.find('おは') > -1:
                    msg += 'おはようございます！'
                elif text.find('こんにちは') > -1 or text.find('こんちゃ') > -1 or text.find('やあ') > -1 or text.find('おっす') > -1:
                    msg += 'こんにちは！'
                elif text.find('こんばん') > -1 or text.find('ばんわ') > -1:
                    msg += 'こんばんは！'
                elif text.find('おつ') > -1 or text.find('疲') > -1 or text.find('お先') > -1 or text.find('おち') > -1 or text.find('落ち') > -1:
                    msg += 'おつかれさまです〜'
                elif text.find('自己紹介して') > -1:
                    msg = 'はい！はじめまして。おががさんに作られたヒヨッ子botの1_1と申します。趣味は素数を数えることです。皆さんのお役に立てすようにがんばりますので、どうぞよろしくお願いします！:cloud:'
                elif text.find('help') > -1 or text.find('-h') > -1:
                    msg += 'https://discordapp.com/channels/407045885281828877/407050154315874315/558382007433035786'
                elif text.find('って何') > -1:
                    msg += wikipediaSearch(text)
                elif text.find('天気') > -1:
                    msg += getWeatherInformation(text)
                elif text.find('は素数') > -1:
                    msg += primarity_test(text, 50)
                else:
                    msg += 'その言葉は知らなかったから調べたよ。\n' + wikipediaSearch(text)
                # メッセージが送られてきたチャンネルへメッセージを送ります
                await client.send_message(message.channel, msg)
                return msg
            except Exception as e:
                print(e)
                raise e

# Get Weather Infomation
def getWeatherInformation(text):
    weather_api_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    response_string = ''
    city_id = ''
    if text.find('長野') > -1:
        city_id = '200010'
    elif text.find('大阪') > -1:
        city_id = '270000'
    elif text.find('東京') > -1:
        city_id = '130010'
    elif text.find('北海道') > -1 or text.find('札幌') > -1:
        city_id = '016010'
    elif text.find('愛知') > -1 or text.find('名古屋') > -1:
        city_id = '230010'
    elif text.find('佐賀') > -1:
        city_id = '410010'
    else:
        city_id = '130010'
        response_string += '場所が聞き取れなかったので取り敢えず'

    try:
        params = {'city':city_id}
        response = requests.get(weather_api_url,params=params)
        response_dict = json.loads(response.text)
        title = response_dict["title"]
        description = response_dict["description"]["text"]
        response_string += title + "です！\n\n"
        forecasts_array = response_dict["forecasts"]
        forcast_array = []
        for forcast in forecasts_array:
            telop = forcast["telop"]
            telop_icon = ''
            if telop.find('雪') > -1:
                telop_icon = ':showman:'
            elif telop.find('雷') > -1:
                telop_icon = ':thunder_cloud_and_rain:'
            elif telop.find('晴') > -1:
                if telop.find('曇') > -1:
                    telop_icon = ':partly_sunny:'
                elif telop.find('雨') > -1:
                    telop_icon = ':partly_sunny_rain:'
                else:
                    telop_icon = ':sunny:'
            elif telop.find('雨') > -1:
                telop_icon = ':umbrella:'
            elif telop.find('曇') > -1:
                telop_icon = ':cloud:'
            else:
                telop_icon = ':fire:'

            temperature = forcast["temperature"]
            min_temp = temperature["min"]
            max_temp = temperature["max"]
            temp_text = ''
            if min_temp is not None:
                if len(min_temp) > 0:
                    temp_text += '\n最低気温は' + min_temp["celsius"] + "℃"
            if max_temp is not None:
                if len(max_temp) > 0:
                    temp_text += '\n最高気温は' + max_temp["celsius"] + "℃"

            forcast_array.append(forcast["dateLabel"] + ' ' + telop + telop_icon + temp_text)
        if len(forcast_array) > 0:
            response_string += '\n\n'.join(forcast_array)
        response_string += '\n\n' + description
    except Exception as e:
        response_string = '天気検索でエラーです＞＜ :cold_sweat:\n' + e.message + '\n' + str(e)
    return response_string

# Search from Wikipedia
def wikipediaSearch(text):
    response_string = ''
    wikipedia.set_lang('ja')
    index_st = text.find(' ')
    index_ed = text.find('って何')
    search_text = text[index_st:index_ed]
    search_response = wikipedia.search(search_text)
    print(search_response)
    if len(search_response) > 0:
        try:
            wiki_page = wikipedia.page(search_response[0])
        except Exception as e:
            try:
                wiki_page = wikipedia.page(search_response[1])
            except Exception as e:
                response_string = 'お探しの言葉ではエラーを起こしました！:cold_sweat:\n' + e.message + '\n' + str(e)
        response_string = '説明しよう！\n'
        response_string += wiki_page.content[0:200] + '.....\n'
        response_string += wiki_page.url
    else:
        response_string = '今はまだ見つけられないンゴ…でも頑張って見つけられるようになるゾ〜！'

    return response_string

# Miller-Rabin Primality Test
def primarity_test(text, k):
    response_string = ''
    index_st = text.find(' ')
    index_ed = text.find('は素数')
    q = int(text[index_st:index_ed])
    if q == 2:
        response_string = str(q) + 'は素数です！:laughing:'
        return response_string
    if q < 2 or q & 1 == 0:
        response_string = str(q) + 'は素数じゃないです！:rage:'
        return response_string

    d = (q - 1) >> 1
    while d & 1 == 0:
        d >>= 1

    for i in range(k):
        a = random.randint(1, q-1)
        t = d
        y = pow(a, t, q)
        while t != q-1 and y != 1 and y != q-1:
            y = pow(y, 2, q)
            t <<= 1
        if y != q-1 and t & 1 == 0:
            response_string = str(q) + 'は素数です！:smile:'
        response_string = str(q) + 'は素数です！:wink:'
    return response_string

client.run(TOKEN)
