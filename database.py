import pymysql
import json
from func import *
from log import logger

def jsonimport():
    # global logger
    try:
        with open("./json/private.json", "r") as f:
            data = json.load(f)["mysql"]
            return data

    except Exception as e:
        logger.error("fail to load data from './json/private.json' ,\nerror:\n"+e)


def hole_dbinsert(pid, timestamp, like_num, reply, url, text="", comment=";"):
    # global logger
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

def holestore(data):
    if type(data) != dict:
        data = data.json()
    if data.get("data") and data["data"]:
        data = data["data"]
    table = dbdata["holetable"]
    try:
        sql = 'select * from {} where pid={}'.format(table, data["pid"])
        cursor.execute(sql)
        if (cursor.rowcount > 0): 
            logger.debug("{} already in".format(data["pid"]))
            return
    except Exception as e:
        logger.error(str(data["pid"]) +" error while search in db:"+ e)
        return 
    hole_dbinsert(
        pid = int(data["pid"]),
        timestamp= int(data["timestamp"]),
        like_num= int(data["likenum"]),
        reply = int(data["reply"]),
        text = data["text"],
        url = data["url"]
    )
    # url TODO:

def holeliststore(responses):
    for response in responses:
        for hole in response["data"]:
            holestore(hole)

def closedb():
    db.close()




dbdata = jsonimport()

db = pymysql.connect(
    host=dbdata["host"],
    user=dbdata["user"],
    password=dbdata["password"],
    port=dbdata["port"],
    db=dbdata['db']
)
cursor = db.cursor()
