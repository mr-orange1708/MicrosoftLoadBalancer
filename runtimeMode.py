from abc import ABC, abstractmethod
from pathlib import Path


class RuntimeMode(ABC):
    def __init__(self, nodeAndTaskContainer: dict) -> None:
        self.nodeAndTaskContainer = nodeAndTaskContainer

    def distributeTask(self, taskName: str, taskType: str, ts: int, duration: int) -> None:
        nodePosition = self.GetNodePositionByTaskType(taskType)
        self.nodeAndTaskContainer[taskType][nodePosition].addNewTask(taskName, taskType, ts, duration)

    @abstractmethod
    def GetNodePositionByTaskType(self, taskType: str) -> int:
        pass
        
        