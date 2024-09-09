import os
import math
import random
import requests

from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()

# 微信公众测试号ID和SECRET
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 可把os.environ结果替换成字符串在本地调试
user_ids = os.environ["USER_ID"].split(',')
template_id = os.environ["TEMPLATE_ID"]
cookie = os.environ["GLADOS_COOKIE"]
# citys = os.environ["CITY"]


# 获取天气和温度
def get_weather(city, appkey):
    # 接口已失效
    # url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    _url = "http://op.juhe.cn/onebox/weather/query"
    _params = {
        "cityname": city,  # 要查询的城市，如：温州、上海、北京
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "dtype": "json",  # 返回数据的格式,xml或json，默认json
    }
    _params = urllib.urlencode(_params)
    res = requests.get(_url, params=_params).json()
    weather = res['result']['future'][0]
    return weather['weather'], weather['temperature']


# 每日一句
def get_words(free_id, free_secret):
    _url = f"https://www.mxnzp.com/api/daily_word/recommend?app_secret={free_secret}&app_id={free_id}"
    words = requests.get(_url)
    if words.status_code == 200:
        return words.json()['data']['content'] - words.json()['data']['author']
    else:
        "牛马人干饭"


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def request_glados(cookie):
    res = {'date': today.date().strftime("%Y-%m-%d")}
    try:
        headers = {
            # 'origin': 'https://glados.rocks',
            'content-Type': 'application/json; charset=utf-8',
            'cookie': cookie,
            'referer': 'https://glados.rocks/console/checkin',
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        }
        _url = "https://glados.rocks/api/user/checkin"
        _body = {"token": "glados.one"}
        _response = requests.post(_url, json=_body, headers=headers, timeout=5)
        if _response.status_code == 200:
            print(_response.json())
            res['message'] = _response.json()["message"]
            if _response.json()['code'] >= 0:
                res['status'] = 'Checkin OK'
                point = _response.json()['list'][0]
                res['point'] = point['change']
                res['balance'] = point['balance']
                _url = "https://glados.rocks/api/user/status"
                _response = requests.get(_url, headers=headers, timeout=5)
                if _response.status_code == 200:
                    _data = _response.json()["data"]
                    res['leftDays'] = _data['leftDays']
                    res['email'] = _data['email']
                    res['days'] = _data['days']
                    res['date'] = _data['system_date']
            else:
                res['status'] = 'Checkin ERROR'
        else:
            res['status'] = 'Checkin ERROR:' + str(_response.status_code)
    except Exception as e:
        print("Exception", e)
        if 'status' not in res:
            res['status'] = 'HTTP ERROR'
        res['message'] = f"签到状态异常：{e}"
    if res['status'] != 'Checkin OK':
        res['leftDays'] = '--'
        res['email'] = '--'
        res['days'] = '--'
        res['point'] = '--'
        res['balance'] = '--'
        if 'message' not in res:
            res['message'] = '--'
    return res


if __name__ == "__main__":
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)

    for i in range(len(user_ids)):
        # wea, tem = get_weather(citys[i])
        # cit, dat = get_city_date(citys[i])
        # words = get_words('free_id','free_secret');
        res = request_glados(cookie)
        data = {
            "date": {"value": res['date'], "color": get_random_color()},
            # "city": {"value": cit, "color": get_random_color()},
            # "weather": {"value": wea, "color": get_random_color()},
            # "temperature": {"value": tem, "color": get_random_color()},
            "status": {"value": res['status'], "color": get_random_color()},
            "msg": {"value": res['message'], "color": get_random_color()},
            "leftDays": {"value": res['leftDays'], "color": get_random_color()},
            "email": {"value": res['email'], "color": get_random_color()},
            "point": {"value": res['point'], "color": get_random_color()},
            "balance": {"value": res['balance'], "color": get_random_color()},
            # "words": {"value": words, "color": get_random_color()}
        }
        res = wm.send_template(user_ids[i], template_id, data)
        print(res)
