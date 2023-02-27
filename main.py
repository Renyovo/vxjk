from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import re

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday2 = os.environ['BIRTHDAYR']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

location_num = os.environ["LOCATION_NUM"]
api_key = os.environ["API_KEY"]


# def get_weather():
#   url = "http://t.weather.sojson.com/api/weather/city/" + city
#   res = requests.get(url).json()
#   weather = res["data"]["forecast"][0]["type"]
#   high = res["data"]["forecast"][0]["high"].replace("高温 ","")
#   low = res["data"]["forecast"][0]["low"].replace("低温 ","")
#   fx = res["data"]["forecast"][0]["fx"] + res["data"]["forecast"][0]["fl"]
#   tem = res["data"]["wendu"] + "℃"
#   notice = res["data"]["forecast"][0]["notice"]
#   quality = res['data']['quality']
#   sunrise = res["data"]["forecast"][0]["sunrise"]
#   sunset = res["data"]["forecast"][0]["sunset"]
#   loca = res["cityInfo"]["city"]
#   return weather,high,low,fx,tem,notice,quality,sunrise,sunset,loca

def get_weather_now():
  rep1 = requests.get(url="https://devapi.qweather.com/v7/weather/now", params={"location": location_num, "key": api_key})
  tem = rep1.json()['now']['temp']
  fx = rep1.json()['now']['windDir'] + rep1.json()['now']['windScale']
  return tem,fx

def get_weather_day():
  rep2 = requests.get(url="https://devapi.qweather.com/v7/weather/3d", params={"location": location_num, "key": api_key})
  sunrise = rep2.json()['daily'][0]['sunrise']
  sunset = rep2.json()['daily'][0]['sunset']
  high = rep2.json()['daily'][0]['tempMax']
  low = rep2.json()['daily'][0]['tempMin']
  day_weather = rep2.json()['daily'][0]['textDay']
  night_weather = rep2.json()['daily'][0]['textNight']
  return sunrise,sunset,high,low,day_weather,night_weather

def get_air():
  rep3 = requests.get(url="https://devapi.qweather.com/v7/air/now", params={"location": location_num, "key": api_key})
  quality = rep3.json()['now']['category']
  mark = rep3.json()['now']['aqi']
  return quality,mark

def get_notice():
  rep4 = requests.get(url="https://devapi.qweather.com/v7/indices/1d", params={"location": location_num, "key": api_key})
  notice = rep4.json()['daily'][0]['text']
  return notice

def get_localation():
  rep5 = requests.get(url="https://geoapi.qweather.com/v2/city/lookup", params={"location": location_num, "key": api_key})
  loca = rep5.json()["location"][0]["name"]
  return loca

def get_day():
  week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  return datetime.now().strftime("%Y年%m月%d日") + " " + week_list[datetime.now().weekday()]

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days


def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
# weather,high,low,fx,tem,notice,quality,sunrise,sunset,loca = get_weather()
tem,fx = get_weather_now()
sunrise,sunset,high,low,day_weather,night_weather = get_weather_day()
quality,mark = get_air()
notice = get_notice()
loca = get_localation()
data = {"data":{"value":get_day(), "color":get_random_color()},"city":{"value":loca, "color":get_random_color()},
        "day_weather":{"value":day_weather, "color":get_random_color()},"night_weather":{"value":night_weather, "color":get_random_color()},
        "high":{"value":high, "color":get_random_color()},"mark":{"value":mark, "color":get_random_color()},
        "low":{"value":low, "color":get_random_color()},"temperature":{"value":tem, "color":get_random_color()},
        "wind":{"value":fx, "color":get_random_color()},"notice":{"value":notice, "color":get_random_color()},
        "sunrise":{"value":sunrise, "color":get_random_color()},"sunset":{"value":sunset, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()},"quality":{"value":quality, "color":get_random_color()},
        "birthday_left2":{"value":get_birthday2(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
