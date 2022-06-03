from multiprocessing import managers
from task import *
import os
import json


class Robot:
    def __init__(self, logger: logging.RootLogger) -> None:
        self.logger = logger
        self.manager = TaskManager(self.logger)
        self.cache_read()

    def cache_read(self):
        cache_path = './cache/cache.json'
        if not os.path.exists(cache_path):
            return
        try:
            print("Cache file is available, \nDo you need to reload your task?: [Y/n]",end="")
            ans = input(" ")
            if ans in ["N","n"]: return
            if ans not in ["\n","","Y","y"]: 
                print("you bad buy!")
                return
            if len(self.manager.tasks) != 0 or self.manager.idPoint != 0:
                raise Exception(
                    "Error robot info found, while reloading tasks from cache:\n" +
                    "self.tasks<len>= {}, self.idPoint= {}".format(
                        len(self.manager.tasks), self.manager.idPoint)
                )
            with open(cache_path, mode='r', encoding='utf-8') as f:
                data = json.load(f)
                for task in data['tasks']:
                    self.manager.reloadTask(task)

        except Exception as e:
            # print("Error:\n",e)
            # pass
            raise e

    def task_run():
        pass

    # def quit(needcache=True):
    def quit(self, neecache = True):
        data = {}
        tasks = []
        for task in self.manager.tasks:
            taskinfo = {}
            taskinfo["id"] = task.id
            taskinfo["state"] = task.state.value
            taskinfo["messager"] = messagerMap[task.messager]
            taskinfo["type"] = task.type
            detail_ = {}
            detail_["createdtime"] = task.detail
            detail_["keywords"] = task.key_words
            taskinfo["detail"] = detail_
            tasks.append(taskinfo)
        data["tasks"] = tasks
        with open("./cache/cache.json", "w", encoding='utf-8') as f:
            json.dump(data, f)

        print("Bye.")

