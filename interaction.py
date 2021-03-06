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

def scroll_show(switch = [False,]):
    while True:
        if switch[0]: break
        time.sleep(0.5)
        cls()
        print("#"*40)
        scrollmsg.show()
        print("#"*40)
    cls()



def show_hole(pid, web:bool = False):
    shown = False
    if not web:
        shown = show_hole_db(pid)
    if not shown:
        show_hole_web(pid)




def inacTask(robot: Robot):
    taskshow(robot)
    while True:
        inpchar = Input()
        if inpchar == "q":
            break
        elif inpchar == " ":
            switch = [False,]
            shower = threading.Thread(target=scroll_show, kwargs= {"switch":switch})
            switchF = threading.Thread(target=touch_switch, kwargs={"label":switch})
            shower.start(), switchF.start()
            shower.join(), switchF.join()
            
            
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
                    print("Task {} begin.".format(choosedtask.id))
                    taskrun = threading.Thread(target=choosedtask.begin)
                    taskrun.start()
                    
                if action == "pause":
                    print("Task {} pause.".format(choosedtask.id))
                    taskrun = threading.Thread(target=choosedtask.pause)
                    taskrun.start()   
        elif "show" in inputinfo:
            inputinfo = inputinfo.split()
            # if len(inputinfo) != 2:
            #     print("Unknown command")
            if "web" in inputinfo:
                show_hole(inputinfo[-1], True)
            else:
                show_hole(inputinfo[-1])
        elif "db" in inputinfo:
            inputinfo = inputinfo.split()
            if "num" in inputinfo:
                searchstatus,searchres = hole_num_search()
                print(searchres)
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
