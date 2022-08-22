from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://wthrcdn.etouch.cn/weather_mini?city=" + city
  res = requests.get(url).json()
  weather = res["data"]["forecast"][0]["type"]
  high = res["data"]["forecast"][0]["high"].replace("高温 ","")
  low = res["data"]["forecast"][0]["low"].replace("低温 ","")
  fx = res["data"]["forecast"][0]["fengxiang"] + re.findall("\d+级",res["data"]["forecast"][0]["fengli"])[0]
  tem = res["data"]["wendu"] + "℃"
  ganmao = res["data"]["ganmao"]
  return weather,high,low,fx,tem,ganmao

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

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, high, low, fx, temperature, ganmao = get_weather()
data = {"data",{"value":get_day(), "color":get_random_color()},"city":{"value":city, "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"high":{"value":high, "color":get_random_color()},"low":{"value":low, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"wind":{"value":fx, "color":get_random_color()},"ganmao":{"value":ganmao, "color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
