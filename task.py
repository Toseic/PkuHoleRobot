from ast import keyword
from enum import Enum
import logging
import time

from prettytable import PrettyTable

from func import *
from messager import *


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
            logger: logging.RootLogger,
            messager=notice,
            state=TaskState.pending,
            cacheload=False) -> None:

        self.state = state
        self.createtime = time.ctime()
        self.id = id
        self.logger = logger
        self.messager = messager

    def begin(self):
        pass

    def run(self):
        if self.state != TaskState.running:
            self.state = TaskState.running
            self.logger.info("task {} begin running.".format(self.id))

    def pause(self):
        if self.state != TaskState.pause:
            self.state = TaskState.pause
            self.logger.info("task {} pause.".format(self.id))

    def finish(self):
        if self.state != TaskState.finished:
            self.state = TaskState.finished
            self.logger.info("task {} finish.".format(self.id))

    def infoLog(self, info):
        self.logger.info(info)

    def messagerSet(self):
        pass

    def message(self, *info):
        self.messager(*info)


class AlarmTask(Task):
    class Mode(enum.Enum):
        match_any = 0
        match_all = 1
        once_match = 2
        continue_match = 3

    def __init__(self, id, logger: logging.RootLogger, messager=notice, state=TaskState.pending, cacheload=False) -> None:
        super().__init__(id, logger, messager, state, cacheload)
        self.key_words = False
        if not cacheload:
            self.key_words_set()
            self.set_mode()
            self.set_sleeptime()
        self.check_record = []
        self.detail = 'key words: '+str(self.key_words)
        self.createdtime = time.ctime()
        self.type = "alarm"

    def __str__(self):
        return "alarm"

    def set_mode(self):
        self.mode = [self.Mode.match_all, self.Mode.once_match]

    def set_sleeptime(self):
        self.sleeptime = 10

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


class TaskManager:
    optionalTasks = {
        'alarm': AlarmTask,
    }

    def __init__(self, logger: logging.RootLogger) -> None:
        self.logger = logger
        self.tasks = []
        self.idPoint = 0

    def createTask(self):
        cls()
        print("Please choose a task type:\n")
        table = PrettyTable(['name', 'describe'])
        for i in self.optionalTasks.keys():
            table.add_row([i, "describe"])
        print(table)
        tasktype = input(": ")
        newtask = self.optionalTasks[tasktype](
            id=self.idPoint,
            logger=self.logger,
        )
        self.idPoint += 1
        self.tasks.append(newtask)
        self.logger.info("Create new task, type:{}, id:{}".format(
            tasktype, newtask.id))

    def reloadTask(self, info):

        if info["id"] != self.idPoint:
            raise Exception(
                "Error id in task:{}\n".format(str(info)) +
                "But self.idPoint is {}".format(self.idPoint)
            )

        newtask = self.optionalTasks[info["type"]](
            id=info["id"],
            logger=self.logger,
            cacheload=True,
        )
        newtask.createdtime = info["detail"]["createdtime"]
        
        newtask.state = TaskState(info["state"])
        newtask.messager = messagerMap[info["messager"]]
        if info["type"] == "alarm":
            newtask.key_words = info["detail"]["keywords"]
        newtask.detail = 'key words: '+str(newtask.key_words)
        self.tasks.append(newtask)
        self.idPoint += 1

    def stopTask(self, id):
        pass

    def pauseTask(self, id):
        pass

    def showTask(self):
        pass

    def cache_read(self):
        pass
