from runtimeMode import RuntimeMode


class QueueSizeMode(RuntimeMode):
    def __init__(self, nodeAndTaskContainer: dict) -> None:
        super().__init__(nodeAndTaskContainer)

    def GetNodePositionByTaskType(self, taskType: str) -> int:
        return self.findNodeWithMinTasks(taskType)

    def findNodeWithMinTasks(self, taskType: str) -> int:
        nodeList = self.nodeAndTaskContainer[taskType]
        numOfMinTasks = len(nodeList[0].taskList)
        retPosition = 0

        for nodePosition in range(1, len(nodeList)):
            if len(nodeList[nodePosition].taskList) < numOfMinTasks:
                retPosition = nodePosition

        return retPosition
