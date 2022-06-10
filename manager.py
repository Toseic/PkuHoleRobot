from task import *


class TaskManager:
    optionalTasks = {
        'alarm': [AlarmTask, "alarm service"],
        'trap': [TrapTask, "crawl hole and store in database."]
    }

    def __init__(self, logger: logging.RootLogger) -> None:
        self.logger = logger
        self.tasks = []
        self.idPoint = 0

    def createTask(self):
        cls()
        print("Please choose a task type:\n")
        table = PrettyTable(['name', 'describe'])
        for key, value in self.optionalTasks.items():
            table.add_row([key, value[1]])
        print(table)
        tasktype = input(": ")
        try:
            newtask = self.optionalTasks.get(tasktype)[0](
                id=self.idPoint,
                logger=self.logger,
            )
        except Exception:
            print("you bad guy.")
            return

        self.idPoint += 1
        self.tasks.append(newtask)
        self.logger.info("Create new task, type:{}, id:{}".format(
            tasktype, newtask.id))
        print("You can press any key to quit.")
        _ = Input()

    def reloadTask(self, info):
        # more feature TODO:
        if info["id"] != self.idPoint:
            raise Exception(
                "Error id in task:{}\n".format(str(info)) +
                "But self.idPoint is {}".format(self.idPoint)
            )

        tasktype = self.optionalTasks.get([info["type"]])
        if not tasktype:
            logger.warn("task type not found. info:\n",str(info))
        newtask = tasktype[0].reloadtask(info)
        self.tasks.append(newtask)
        self.idPoint += 1

    def stopTask(self, id):
        # TODO:
        pass

    def pauseTask(self, id):
        pass

    def pauseallTask(self):
        print("pausing all tasks before quit...")
        for task in self.tasks:
            if task.state == TaskState.running:
                print("task {} pause".format(task.id))
                task.pause()

    def showTask(self):
        pass

    def editTask(self, id, mode):
        try:
            self.tasks[id].set_mode(mode)
            print("success, press any key to quit.")
        except:
            print("error.")

    def infocache(self):
        tasks = []
        for task in self.tasks:
            taskinfo = task.infocache()
            tasks.append(taskinfo)
        return tasks


def taskhelp():
    cls()
    print(
        '''
    help:
    key      function
    s:       task setting
    q:       quit
    n:       create a new task
    r:       refresh window
    space    show crawl detail

    press any key to quit
    '''
    )
    _ = Input()


def taskset(manager: TaskManager):
    # each type of task fit a taskset func TODO:
    cls()
    id = int(input("which task is need to edit? "))
    print(rwc(" match any ", Color.yellow) +
          " / " + rwc("match all", Color.yellow))
    ans1 = input("choose: [0/1] ")
    if ans1 == "":
        ans1 = 1
    try:
        ans1 = int(ans1)
    except:
        print("you bad guy.")
    print(rwc(" once match ", Color.yellow)+" / " +
          rwc("continue match", Color.yellow))
    ans2 = input("choose: [0/1] ")
    if ans2 == "":
        ans2 = 1
    try:
        ans2 = int(ans2)+2
    except:
        print("you bad guy.")
    manager.editTask(id, [ans1, ans2])
    _ = Input()
