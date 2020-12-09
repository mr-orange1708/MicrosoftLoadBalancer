from abc import ABC, abstractmethod
from pathlib import Path


class RuntimeMode(ABC):
    def __init__(self, node_and_task_container: dict) -> None:
        self.node_and_task_container = node_and_task_container

    def distribute_task(self, task_name: str, task_type: str, ts: int, duration: int) -> None:
        node_position = self.get_node_position_by_task_type(task_type)
        self.node_and_task_container[task_type][node_position].add_new_task(task_name, task_type, ts, duration)

    @abstractmethod
    def get_node_position_by_task_type(self, task_type: str) -> int:
        pass
        
        