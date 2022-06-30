import json
import os
from multiprocessing import managers

from manager import TaskManager
from task import *
from log import logger


class Robot:
    def __init__(self) -> None:
        self.manager = TaskManager()
        self.cache_read()

    def cache_read(self):
        cache_path = './cache/cache.json'
        if not os.path.exists(cache_path):
            return
        try:
            print(
                "Cache file is available, \nDo you need to reload your task?: [Y/n]", end="")
            ans = input(" ")
            if ans in ["N", "n"]:
                return
            if ans not in ["\n", "", "Y", "y"]:
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

    def task_run(self):
        pass

    # def quit(needcache=True):
    def quit(self, neecache=True):
        self.manager.pauseallTask()
        data = {}
        data["tasks"] = self.manager.infocache()
        with open("./cache/cache.json", "w", encoding='utf-8') as f:
            json.dump(data, f)

       
