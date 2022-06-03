import enum
import os
import threading

from prettytable import PrettyTable

from robot import Robot
from task import *

inacSuggest = {
    "task": "tasks"
}





def taskshow(robot: Robot):
    cls()
    print(rwc(" "*5+"Press q to quit, SPACE to show detail."+" "*5, 32, 7))
    print(rwc("tasks\n", Color.blue, 1))
    table = PrettyTable(['Id', 'type', 'state','details'])
    for i in robot.manager.tasks:
        table.add_row([i.id, i, i.state,i.detail])
    print(table)


def inacTask(robot: Robot):
    taskshow(robot)
    while True:
        inpchar = Input()
        if inpchar == "q":
            break
        if inpchar == " ":
            print("detail")
        if inpchar == "r":
            taskshow(robot)
        if inpchar == "n":
            robot.manager.createTask()
            taskshow(robot)
    cls()


def inacFrame(robot: Robot = None):
    while True:
        print(">", end='')
        inputinfo = input(" ")
        if inputinfo in ["\n", ""]:
            continue
        elif inputinfo == "help":
            print("help info")
        elif  inputinfo == "tasks":
            inacTask(robot)
        elif "task" in inputinfo:
            inputinfo = inputinfo.split()
            if len(inputinfo) != 3:
                print("Unknown command")
            else:
                id, action = int(inputinfo[1]), inputinfo[2]
                choosedtask = robot.manager.tasks[id]
                if action == "begin": 
                    taskrun = threading.Thread(target=choosedtask.begin)
                    taskrun.start()
                    # choosedtask.begin()
                if action == "pause":
                    taskrun = threading.Thread(target=choosedtask.pause)
                    taskrun.start()                   
        elif inputinfo == "quit":
            print("bye~")
            break
        # suggest
        else:
            print("Unknown command: '{}'".format(inputinfo))
            for key, value in inacSuggest.items():
                if inputinfo == key:
                    print(" Do you mean :'{}' ?".format(value))


if __name__ == '__main__':
    inacFrame()
    # pass
