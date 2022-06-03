import logging
import time


def Logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # logpath = "./log/"
    # logfile = logpath + rq + ".log"
    # fh = logging.FileHandler(logfile, mode='w')
    # fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
