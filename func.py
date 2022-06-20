# coding:utf-8
import datetime
import enum
import json
import os
from ctypes import *

import requests


dll = CDLL('./dll/input_mac.so')

inacSuggest = {
    "task": "tasks"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,km;q=0.8',
    'Referer': 'https://pkuhelper.pku.edu.cn/hole/',

}


class Mode(enum.Enum):
    Create = "dopost"
    Comment = "docomment"
    Attention = "attention"
    Pull_comment = "getcomment"
    Pull_hole = "getone"


class Attention(enum.Enum):
    Attention = 1
    De_Attention = 0


class Show(enum.Enum):
    Need = 1
    DontNeed = 0


class Color(enum.Enum):
    blac = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan_blue = 36
    white = 37


def rwc(show_str, color_code, status_code=0):
    '''
    color: ['black','red','green','yellow','blue','magenta','cyan_blue','white']
    '''
    # 前景色: 30（黑色）、31（红色）、32（绿色）、 33（黄色）
    # 34（蓝色）、35（洋 红）、36（青色）、37（白色）
    # status_code: 1:加深 7：背景反色
    show_str = str(show_str)
    # print(type(color_code))
    if type(color_code) == type(Color.blue):
        color_code = color_code.value
    return "\033[{};{}m".format(status_code, color_code)+show_str+"\033[0;0m"

def Input():
    return chr(dll.Input())


def cls():
    os.system("clear")


def jsapiver_get():
    now = datetime.datetime.now()
    stamp = int(now.timestamp() / 7200)*2
    return "201027113050-" + str(stamp)


def url_get_3(mode: Mode):
    base_url = "https://pkuhelper.pku.edu.cn/services/pkuhole/api.php?action={}&PKUHelperAPI=3.0&jsapiver={}&user_token={}".format(
        mode.value, '{}', '{}')
    apier = jsapiver_get()
    return base_url.format(apier, token)


def url_get_4(mode: Mode, pid: int):
    base_url = "https://pkuhelper.pku.edu.cn/services/pkuhole/api.php?action={}&pid={}&PKUHelperAPI=3.0&jsapiver={}&user_token={}".format(
        mode.value, '{}', '{}', '{}')
    apier = jsapiver_get()
    return base_url.format(pid, apier, token)


def hole_creater(text):
    data = {
        'text': text,
        'type': 'text',
        'user_token': token,
    }
    url = url_get_3(Mode.Create)
    response = requests.post(
        url=url, data=data, headers=headers, proxies=my_proxies)
    return response


def comment(text, pid):
    data = {
        'pid': pid,
        'text': text,
        'user_token': token,
    }
    url = url_get_3(Mode.Comment)
    response = requests.post(
        url=url, data=data, headers=headers, proxies=my_proxies)
    return response


def attention(pid, mode: Attention):
    data = {
        'user_token': token,
        'pid': pid,
        'switch': mode.value,
    }
    url = url_get_3(Mode.Attention)
    response = requests.post(
        url=url, data=data, headers=headers, proxies=my_proxies)
    return response


def get_comment(pid):
    url = url_get_4(Mode.Pull_comment, pid)
    response = requests.get(url=url, headers=headers, proxies=my_proxies)
    return response


def get_hole(pid):
    url = url_get_4(Mode.Pull_hole, pid)
    response = requests.get(url=url, headers=headers, proxies=my_proxies)
    return response


def show_hole_web(pid):
    res_hole = get_hole(pid).json()
    res_comment = get_comment(pid).json()
    # empty result TODO:
    print("Pid:{} | time:{} | star:{} | comments:{} | from:web".format(
        res_hole['data']['pid'], 
        datetime.datetime.fromtimestamp(int(res_hole['data']['timestamp'])),
        res_hole['data']['likenum'], 
        res_hole['data']['reply']))
    print("[洞主]", res_hole['data']['text'])
    for i in res_comment['data']:
        print(i['text'])


def info_merge(info_):
    fina = {}
    info_ = info_[0]['data']
    for hole in info_:
        fina[int(hole['pid'])] = hole['text']
    return fina

def point_check(info, pidpoint):
    before, after = False, False
    for list in info:
        datas = list['data']
        for data in datas:
            if int(data['pid']) == pidpoint:
                return True            
            elif int(data['pid']) < pidpoint:
                before = True
            elif int(data['pid']) > pidpoint:
                after = True

    if before and after:
        return True

    return False

def crawl_list(deep=1, merge=False, pidpoint=None):
    '''
    pidpoint: crawl result must include pidpoint
    '''
    # if merge and storeindb:
    #     raise Exception("error: [merge] and [storeindb] are both True!")
    url = 'https://pkuhelper.pku.edu.cn/services/pkuhole/api.php?action=getlist&p={}&PKUHelperAPI=3.0&jsapiver={}&user_token={}'
    url = url.format('{}', jsapiver_get(), token)
    info = []
    for i in range(0, deep):
        url_i = url.format(i+1)
        response = requests.get(url=url_i, headers=headers, proxies=my_proxies)
        info.append(response.json())
    if pidpoint and pidpoint != -1:
        checkres = point_check(info, pidpoint)
        if not checkres:
            return crawl_list(deep=deep+1, merge=merge, pidpoint=pidpoint)
    newpoint = int(info[0]['data'][0]['pid'])
    if merge:
        info = info_merge(info)
    return info,newpoint


def get_json():
    with open("./json/private.json", "r") as gj:
        return json.load(gj)


data = get_json()
token = data["token"]
my_proxies = data["proxies"]

