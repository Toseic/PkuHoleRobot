from encodings import search_function
import pymysql
import json
from func import *
from log import logger

def jsonimport():
    try:
        with open("./json/private.json", "r") as f:
            data = json.load(f)["mysql"]
            return data

    except Exception as e:
        logger.error("fail to load data from './json/private.json' ,\nerror:\n"+e)


def hole_dbinsert(pid, timestamp, like_num, reply, url, text="", comment=";"):
    data = {
        'pid': pid,
        "timestamp": timestamp,
        "like_num": like_num,
        "reply": reply,
        "text": text,
        "comment": comment,
        "url" : url
    }
    table = dbdata["holetable"]
    keys = ", ".join(data.keys())
    values = ", ".join(["%s"]*len(data))
    sql = "insert into {}({}) values ({})".format(
        table, keys, values
    )
    try:
        if cursor.execute(sql, tuple(data.values())):
            logger.debug(str(pid)+" insert successful")
            # print(str(pid)+" insert successful")
            db.commit()
    except Exception as e:
        logger.error(str(pid) +" error while insert:"+ e)
        # print(str(pid) +" error while insert:"+ e)
        db.rollback()

def pid_search(table:str, pid): #comment search TODO:
    '''
    ans number = 0: false
    ans number > 0: (pid, timestrap, like_num, reply, text, comment, url)
    '''
    sql = 'select * from {} where pid={}'.format(table, pid)
    try:
        cursor.execute(sql)
    except Exception as e:
        logger.error("error happend while search pid=[{}] in db {}. ".format(pid, table)+e)
        return False, "somwthing wrong happend while searching in database."
    if (cursor.rowcount == 0): 
        return False, None
    else:
        return True, cursor.fetchone()
    

def hole_num_search():
    sql = 'select * from {}'.format(dbdata["holetable"])
    try:
        cursor.execute(sql)
    except Exception as e:
        logger.error("error happend while search hole-num in db {}. ".format(dbdata["holetable"])+e)
        return False, "somwthing wrong happend while searching in database."
    return True, cursor.rowcount
    
def holestore(data):
    if type(data) != dict:
        data = data.json()
    if data.get("data") and data["data"]:
        data = data["data"]
    
    search_ans = pid_search(dbdata["holetable"], data["pid"])
    if search_ans[0]:
        logger.debug("{} already in".format(data["pid"]))
        return False   
 
    hole_dbinsert(
        pid = int(data["pid"]),
        timestamp= int(data["timestamp"]),
        like_num= int(data["likenum"]),
        reply = int(data["reply"]),
        text = data["text"],
        url = data["url"]
    )

def holeliststore(responses):
    for response in responses:
        for hole in response["data"]:
            holestore(hole)

def closedb():
    db.close()

def show_hole_db(pid):
    if type(pid) == str:
        try:
            pid = int(pid)
        except:
            print("something is wrong in your pid.")
            return False
    
    res = pid_search(dbdata["holetable"], pid)
    if not res[0]: return False
    print("Pid:{} | time:{} | star:{} | comments:{} | from:database".format(
        res[1][0], 
        datetime.datetime.fromtimestamp(res[1][1]),
        res[1][2], 
        res[1][3]))
    print("[洞主]", res[1][4])
    return True
    # show comment

dbdata = jsonimport()

db = pymysql.connect(
    host=dbdata["host"],
    user=dbdata["user"],
    password=dbdata["password"],
    port=dbdata["port"],
    db=dbdata['db']
)
cursor = db.cursor()
