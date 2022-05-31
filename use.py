#coding:utf-8
import requests
import datetime,json,enum

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


def jsapiver_get():
    now = datetime.datetime.now()
    stamp = int(now.timestamp() / 7200)*2
    return "201027113050-" + str(stamp)



def url_get_3(mode: Mode):
    base_url = "https://pkuhelper.pku.edu.cn/services/pkuhole/api.php?action={}&PKUHelperAPI=3.0&jsapiver={}&user_token={}".format(mode.value,'{}','{}')
    apier = jsapiver_get()
    return base_url.format(apier, token)

def url_get_4(mode: Mode, pid:int):
    base_url = "https://pkuhelper.pku.edu.cn/services/pkuhole/api.php?action={}&pid={}&PKUHelperAPI=3.0&jsapiver={}&user_token={}".format(mode.value,'{}','{}','{}')
    apier = jsapiver_get()
    return base_url.format(pid, apier, token)

def hole_creater(text):
    data = {
        'text':text,
        'type':'text',
        'user_token':token,
    }
    url = url_get_3(Mode.Create)
    response = requests.post(url=url, data=data, headers=headers, proxies=my_proxies)
    return response
    # print(response.text)

def comment(text, pid):
    data = {
        'pid':pid,
        'text':text,
        'user_token':token,
    }
    url = url_get_3(Mode.Comment)
    response = requests.post(url=url, data=data, headers=headers, proxies=my_proxies)
    return response

def attention(pid, mode: Attention):
    data = {
        'user_token':token,
        'pid':pid,
        'switch':mode.value,
    }
    url = url_get_3(Mode.Attention)
    response = requests.post(url=url, data=data, headers=headers, proxies=my_proxies)
    return response


def get_comment(pid):
    url = url_get_4(Mode.Pull_comment, pid)
    response = requests.get(url=url, headers=headers, proxies=my_proxies)
    return response

def get_hole(pid):
    url = url_get_4(Mode.Pull_hole, pid)
    response = requests.get(url=url, headers=headers, proxies=my_proxies)
    return response


def show_hole(pid):
    res_hole = get_hole(pid).json()
    res_comment = get_comment(pid).json()

    print("Pid:{} | star:{} | comments:{}".format(res_hole['data']['pid'],res_hole['data']['likenum'],res_hole['data']['reply']))
    print("[洞主]",res_hole['data']['text'])
    for i in res_comment['data']:
        print(i['text'])

def get_json():
    with open("./private.json","r") as gj:
        return json.load(gj)

if __name__ == "__main__":
    data = get_json()
    token = data["token"]
    my_proxies = data["proxies"]

