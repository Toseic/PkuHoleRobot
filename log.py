import logging
import time
import datetime 
################## scroll ##################

class scrollMsg():
    def __init__(self) -> None:
        self.msgs = []
    def editor(self, new_msg: str):
        self.msgs.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S  ') +new_msg)
        if len(self.msgs) > 5:
            self.msgs = self.msgs[-5:]
    def show(self):
        # print(rwc("*"*30,Color.yellow))
        for msg in self.msgs:
            print(" "*2+msg)
        # print(rwc("*"*30,Color.yellow))

scrollmsg = scrollMsg()

################## scroll ##################


################## logger ##################

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logpath = "./log/"
logfile = logpath + rq + ".log"
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch.setFormatter(formatter)
logger.addHandler(ch)

################## logger ##################
