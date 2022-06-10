import time
from enum import Enum

from prettytable import PrettyTable

from database import *
from func import *
from messager import *
from log import logger


class TaskState(Enum):
    pending = -2
    pause = -1
    running = 0
    finished = 1


messagerMap = {
    "notice": notice,
    notice: "notice",
}


class Task:
    def __init__(
            self, id,
            messager=notice,
            state=TaskState.pending,
            ) -> None:

        self.state = state
        self.createtime = time.ctime()
        self.id = id
        self.messager = messager
        self.type = 'task'

    def __str__(self):
        return self.type

    def begin(self):
        pass

    def set_sleeptime(self, time = None):
        if not time:
            self.sleeptime = int(input("sleep time?: "))
        else:
            try:
                self.sleeptime = int(time)
            except:
                print("error")

    def run(self):
        if self.state != TaskState.running:
            self.state = TaskState.running
            logger.info("task {} begin running.".format(self.id))

    def pause(self):
        if self.state != TaskState.pause:
            self.state = TaskState.pause
            logger.info("task {} pause.".format(self.id))

    def finish(self):
        if self.state != TaskState.finished:
            self.state = TaskState.finished
            logger.info("task {} finish.".format(self.id))

    def infoLog(self, info):
        logger.info(info)

    def messagerSet(self):
        # TODO:
        pass

    def message(self, *info):
        self.messager(*info)


class AlarmTask(Task):
    class Mode(enum.Enum):
        match_any = 0
        match_all = 1
        once_match = 2
        continue_match = 3
    # class Modestr(enum.Enum):
    #     match_any = 'match_any'
    #     match_all = 'match_all'
    #     once_match = 'once_match'
    #     continue_match = 'continue_match'

    def __init__(self, id, messager=notice, state=TaskState.pending, cacheload=False) -> None:
        super().__init__(id, messager, state)
        self.key_words = False
        self.mode = []
        if not cacheload:
            self.key_words_set()
            self.set_mode()
            self.set_sleeptime()
        self.check_record = []
        self.detail = 'key words: '+str(self.key_words)
        self.createdtime = time.ctime()
        self.type = "alarm"
        if not cacheload:
            print("your task[{}] is created, \nIt's mode is defult to be [".format(self.id)
                + rwc("match all", Color.yellow) +
                "] and ["+rwc("once match", Color.yellow)+"]"
                )

    def modestr(self):
        return (
            str(self.mode[0]) + " "
            + str(self.mode[1])
        )

    def set_mode(self, mode_=None):
        if not mode_:
            self.mode = [self.Mode.match_all, self.Mode.once_match]
        else:
            mode1, mode2 = mode_[0], mode_[1]
            self.mode = [self.Mode(mode1), self.Mode(mode2)]

    def key_words_set(self):
        info = input("input key words(split by ^):\n")
        if "^" in info:
            self.key_words = info.split("^")
        elif info:
            self.key_words = [info, ]
        else:
            print("your input is empty. Input again:\n")
            self.key_words_set()

    def match(self, info: str) -> bool:
        match_record = []
        for i in self.key_words:
            if i in info:
                match_record.append(True)
            else:
                match_record.append(False)
        if self.mode[0] == self.Mode.match_all:
            if False in match_record:
                return False
            return True
        if self.mode[0] == self.Mode.match_any:
            if True in match_record:
                return True
            return False

    def return_info(self, pid):
        self.messager("Mached.")
        show_hole(pid)

    def begin(self):
        if not self.key_words:
            raise Exception("key words error.")
        super().run()
        while self.state == TaskState.running:
            hole_list = crawl_list()
            self.infoLog("crawl list(deep=1).")
            for pid, hole in hole_list.items():
                if pid in self.check_record:
                    continue
                self.check_record.append(pid)
                if self.match(hole):
                    self.return_info(pid)
                    if self.mode[1] == self.Mode.once_match:
                        self.finish()

            time.sleep(self.sleeptime)

    def infocache(self):
        taskinfo = {}
        taskinfo["id"] = self.id
        taskinfo["messager"] = messagerMap[self.messager]
        taskinfo["type"] = self.type
        taskinfo["sleeptime"] = self.sleeptime
        detail_ = {}
        detail_["keywords"] = self.key_words
        taskinfo["detail"] = detail_
        taskinfo["mode"] = [self.mode[0].value, self.mode[1].value]
        return taskinfo

    def reloadtask(info):
        newtask = AlarmTask(
            id=info["id"],
            cacheload=True,
        )
        newtask.messager = messagerMap[info["messager"]]
        newtask.key_words = info["detail"]["keywords"]
        newtask.detail = 'key words: '+str(newtask.key_words)
        newtask.set_mode(info["mode"])
        newtask.set_sleeptime(info["sleeptime"])
        return newtask


class TrapTask(Task):
    def __init__(self, id, messager=notice, state=TaskState.pending, cacheload=False) -> None:
        super().__init__(id, messager, state)
        self.sleeptime = 20
        if not cacheload:
            self.set_sleeptime()
            print("your task[{}] is created, \nIt's sleeptime is defult to be {}".format(self.id, self.sleeptime))
        self.detail = "crawl time gap: {}".format(self.sleeptime)
        self.type = "trap"

    def begin(self):
        super().run()
        while self.state == TaskState.running:
            holeliststore(crawl_list())
            self.infoLog("task:Traptask | crawl list(deep=1)")
            time.sleep(self.sleeptime)

    def modestr(self):
        return "simple mode"

    def infocache(self):
        taskinfo = {}
        taskinfo["id"] = self.id
        taskinfo["type"] = self.type
        taskinfo["sleeptime"] = self.sleeptime
        return taskinfo

    def reloadtask(info):
        newtask = TrapTask(
            id=info["id"],
            cacheload=True,
        )
        newtask.set_sleeptime(info["sleeptime"])
        newtask.detail = "crawl time gap: {}".format(newtask.sleeptime)
        newtask.type = "trap"
        return newtask
