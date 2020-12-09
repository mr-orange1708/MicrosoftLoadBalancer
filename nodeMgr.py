import collections
import time
from threading import Thread, Lock


class NodeMgr():
    class Task:
        def __init__(self, task_name: str, task_type: str, ts: int, duration: int) -> None:
            self.task_name = task_name
            self.task_type = task_type
            self.ts = ts
            self.duration = duration

    def __init__(self, node_name: str, task_type: str) -> None:
        self.node_name = node_name
        self.task_type = task_type
        self.continue_running = True
        self.mutex = Lock()
        self.task_list = collections.deque()
        self.thread = Thread(target = self.node_run)
        self.thread.start()

    def add_new_task(self, task_name: str, task_type: str, ts: int, duration: int) -> None:
        new_task = self.Task(task_name, task_type, ts, duration)
        self.mutex.acquire()
        self.task_list.append(new_task)
        self.mutex.release()
    
    def get_next_task(self) -> Task:
        self.mutex.acquire()
        ret_task = self.task_list.popleft()
        self.mutex.release()
        return ret_task

    def is_task_list_empty(self) -> bool:
        return len(self.task_list) == 0

    def stop_running(self) -> None:
        while not self.is_task_list_empty():
            time.sleep(5)
        self.continue_running = False
        self.thread.join()

    def node_run(self) -> None:
        while self.continue_running:
            if (self.is_task_list_empty()):
                time.sleep(0.5)
            else:
                current_task = self.get_next_task()
                self.mutex.acquire()
                print ("Executed task = " + current_task.task_name + ", type = " + current_task.task_type + ", on node = " + self.node_name + 
                    ", started at t = " + str(current_task.ts))
                self.mutex.release()
                time.sleep(current_task.duration)

