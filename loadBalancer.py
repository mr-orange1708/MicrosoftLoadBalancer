import json
import importlib
import time
from pathlib import Path
from nodeMgr import NodeMgr
from roundRobinMode import RoundRobinMode
from queueSizeMode import QueueSizeMode


class LoadBalancer:
    def __init__(self) -> None:
        self.nodes_and_tasks_by_task_type = {}
        self.run_time_mode = None

    def read_nodes_from_file(self, file_path: str) -> tuple:
        json_file = Path(file_path)

        try:
            if not json_file.exists() or not json_file.is_file():
                return (False, "The given json path is not valid")

            with json_file.open() as f:
                json_data = json.load(f)
        except Exception as e:
            return (False, "Exception accrued: " + str(e))
            
        for node in json_data["nodes"]:
            self.add_new_node(node["nodeName"], node["taskType"])

        return (True, "The json data has been read")

    def read_tasks_from_file(self, file_path: str) -> tuple:
        text_file = Path(file_path)
        previous_time = 0

        if not text_file.exists() or not text_file.is_file():
            return (False, "The given text file path is not valid")

        self.run_time_mode = QueueSizeMode(self.nodes_and_tasks_by_task_type)

        with text_file.open() as f:
            for line in f:
                current_json = json.loads(line)
                
                if current_json["ts"] < previous_time:
                    continue
                elif current_json["ts"] > previous_time:
                    time.sleep(current_json["ts"] - previous_time)
                    previous_time = current_json["ts"]

                self.run_time_mode.distribute_task(current_json["taskName"], current_json["taskType"], current_json["ts"], current_json["duration"])

        return (True, "All tasks data has been read")

    def add_new_node(self, node_name: str, task_type: str) -> None:
        new_node = NodeMgr(node_name, task_type)
        
        if task_type not in self.nodes_and_tasks_by_task_type:
            self.nodes_and_tasks_by_task_type[task_type] = [new_node]
        else:
            self.nodes_and_tasks_by_task_type[task_type].append(new_node)

    def stop_running(self) -> None:
        for task_type in self.nodes_and_tasks_by_task_type:
            for node in self.nodes_and_tasks_by_task_type[task_type]:
                node.stopRunning()
