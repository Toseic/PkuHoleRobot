import enum
import os
import threading

from prettytable import PrettyTable

from robot import Robot
from task import *
from manager import *

inacSuggest = {
    "task": "tasks"
}



def taskshow(robot: Robot):
    cls()
    print(rwc(" "*5+"Press h for help, SPACE to show detail."+" "*5, 32, 7))
    print(rwc("tasks\n", Color.blue, 1))
    table = PrettyTable(['Id', 'type', 'state','details','mode'])
    for i in robot.manager.tasks:
        table.add_row([i.id, i, i.state, rwc(i.detail, Color.blue), rwc(i.modestr(), Color.yellow)])
    print(table)


def inacTask(robot: Robot):
    taskshow(robot)
    while True:
        inpchar = Input()
        if inpchar == "q":
            break
        elif inpchar == " ":
            print("detail")
            # TODO: detail
        elif inpchar == "r":
            taskshow(robot)
        elif inpchar == "n":
            robot.manager.createTask()
        elif inpchar == "h":
            taskhelp()
        elif inpchar == "s":
            taskset(robot.manager)
            
        taskshow(robot)
    cls()


def inacFrame(robot: Robot):
    while True:
        print(">", end='')
        inputinfo = input(" ")
        if inputinfo in ["\n", ""]:
            continue
        elif inputinfo == "help":
            print("help info")
            #  help info  TODO:
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
        elif "quit" in inputinfo:
            if "-hard" in inputinfo:
                robot.quit(False)
                break
            robot.quit()
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
