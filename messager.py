import ctypes
import time
from plyer import notification
from log import logger


def sound():
    player = ctypes.windll.kernel32
    for _ in range(7):
        player.Beep(1000, 500)
        time.sleep(0.1)


def notice(message: str, title: str = "PkuHoleRobot messager",  opensound: bool = False, timeout=5):
    print("send")
    notification.notify(
        title=title,
        message=message,
        timeout=timeout
    )
    if opensound:
        sound()


def remote_notice():
    pass
