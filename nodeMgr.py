import collections
import time
from threading import Thread, Lock


class NodeMgr():
    class Task:
        def __init__(self, taskName: str, taskType: str, ts: int, duration: int) -> None:
            self.taskName = taskName
            self.taskType = taskType
            self.ts = ts
            self.duration = duration

    def __init__(self, nodeName: str, taskType: str) -> None:
        self.nodeName = nodeName
        self.taskType = taskType
        self.continueRunning = True
        self.mutex = Lock()
        self.taskList = collections.deque()
        self.thread = Thread(target = self.nodeRun)
        self.thread.start()

    def addNewTask(self, taskName: str, taskType: str, ts: int, duration: int) -> None:
        newTask = self.Task(taskName, taskType, ts, duration)
        self.mutex.acquire()
        self.taskList.append(newTask)
        self.mutex.release()
    
    def getNextTask(self) -> Task:
        self.mutex.acquire()
        retTask = self.taskList.popleft()
        self.mutex.release()
        return retTask

    def isTaskListEmpty(self) -> bool:
        return len(self.taskList) == 0

    def stopRunning(self) -> None:
        while not self.isTaskListEmpty():
            time.sleep(5)
        self.continueRunning = False
        self.thread.join()

    def nodeRun(self) -> None:
        while self.continueRunning:
            if (self.isTaskListEmpty()):
                time.sleep(0.5)
            else:
                currentTask = self.getNextTask()
                self.mutex.acquire()
                print ("Executed task = " + currentTask.taskName + ", type = " + currentTask.taskType + ", on node = " + self.nodeName + 
                    ", started at t = " + str(currentTask.ts))
                self.mutex.release()
                time.sleep(currentTask.duration)

