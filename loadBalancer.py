import json
import importlib
import time
from pathlib import Path
from nodeMgr import NodeMgr
from roundRobinMode import RoundRobinMode


class LoadBalancer:
    def __init__(self) -> None:
        self.nodesAndTasksByTaskType = {}
        self.runtimeMode = None

    def read_nodes_from_file(self, filePath: str) -> tuple:
        jsonFile = Path(filePath)

        try:
            if not jsonFile.exists() or not jsonFile.is_file():
                return (False, "The given json path is not valid")

            with jsonFile.open() as f:
                jsonData = json.load(f)
        except Exception as e:
            return (False, "Exception accrued: " + str(e))
            
        for node in jsonData["nodes"]:
            self.add_new_node(node["nodeName"], node["taskType"])

        return (True, "The json data has been read")

    def read_tasks_from_file(self, filePath: str) -> tuple:
        textFile = Path(filePath)
        previousTime = 0

        if not textFile.exists() or not textFile.is_file():
            return (False, "The given text file path is not valid")

        self.runtimeMode = RoundRobinMode(self.nodesAndTasksByTaskType)

        with textFile.open() as f:
            for line in f:
                currentJson = json.loads(line)
                
                if currentJson["ts"] < previousTime:
                    continue
                elif currentJson["ts"] > previousTime:
                    time.sleep(currentJson["ts"] - previousTime)
                    previousTime = currentJson["ts"]

                self.runtimeMode.distributeTask(currentJson["taskName"], currentJson["taskType"], currentJson["ts"], currentJson["duration"])

        return (True, "All tasks data has been read")

    def add_new_node(self, nodeName: str, taskType: str) -> None:
        newNode = NodeMgr(nodeName, taskType)
        
        if taskType not in self.nodesAndTasksByTaskType:
            self.nodesAndTasksByTaskType[taskType] = [newNode]
        else:
            self.nodesAndTasksByTaskType[taskType].append(newNode)

    def stop_running(self) -> None:
        for taskType in self.nodesAndTasksByTaskType:
            for node in self.nodesAndTasksByTaskType[taskType]:
                node.stopRunning()
