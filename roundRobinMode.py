from runtimeMode import RuntimeMode


class RoundRobinMode(RuntimeMode):
    def __init__(self, nodeAndTaskContainer: dict) -> None:
        super().__init__(nodeAndTaskContainer)
        self.prevNodeByTaskType = {}

        for taskType in nodeAndTaskContainer:
            self.prevNodeByTaskType[taskType] = -1
    
    def GetNodePositionByTaskType(self, taskType: str) -> int:
        return self.findNextNodeByOrder(taskType)

    def findNextNodeByOrder(self, taskType: str) -> int:
        currentNodeByTaskType = self.prevNodeByTaskType[taskType] + 1

        if currentNodeByTaskType == len(self.nodeAndTaskContainer[taskType]):
            currentNodeByTaskType = 0

        self.prevNodeByTaskType[taskType] = currentNodeByTaskType

        return currentNodeByTaskType
