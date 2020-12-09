import json
import time
import imp
import os
from pathlib import Path
from nodeMgr import NodeMgr


class LoadBalancer:
    def __init__(self) -> None:
        self.nodes_and_tasks_by_task_type = {}

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

    def read_tasks_from_file(self, file_path: str, runtime_mode_file_path: str) -> tuple:
        text_file = Path(file_path)
        previous_time = 0

        if not text_file.exists() or not text_file.is_file():
            return (False, "The given text file path is not valid")
        
        run_time_mode = self.get_runtime_mode_dynamically(runtime_mode_file_path)

        if run_time_mode == None:
            return (False, "Wrong runtime mode input")

        with text_file.open() as f:
            for line in f:
                current_json = json.loads(line)
                
                if current_json["ts"] < previous_time:
                    continue
                elif current_json["ts"] > previous_time:
                    time.sleep(current_json["ts"] - previous_time)
                    previous_time = current_json["ts"]

                run_time_mode.distribute_task(current_json["taskName"], current_json["taskType"], current_json["ts"], current_json["duration"])

        return (True, "All tasks data has been read")

    def get_runtime_mode_dynamically(self, runtime_mode_file_path: str):
        class_inst = None
        class_name = Path(runtime_mode_file_path).stem
        class_name = class_name[0].upper() + class_name[1: ]
        mod_name,file_ext = os.path.splitext(os.path.split(runtime_mode_file_path)[-1])
        
        try:
            if file_ext.lower() == '.py':
                py_mod = imp.load_source(mod_name, runtime_mode_file_path)
            else:
                print("Wrong input file name for runtime mode")
                return None

            if hasattr(py_mod, class_name):
                class_inst = getattr(py_mod, class_name)(self.nodes_and_tasks_by_task_type)

        except Exception as e:
            print("Exception accrued: " + str(e))

        return class_inst

    def add_new_node(self, node_name: str, task_type: str) -> None:
        new_node = NodeMgr(node_name, task_type)
        
        if task_type not in self.nodes_and_tasks_by_task_type:
            self.nodes_and_tasks_by_task_type[task_type] = [new_node]
        else:
            self.nodes_and_tasks_by_task_type[task_type].append(new_node)

    def stop_running(self) -> None:
        for task_type in self.nodes_and_tasks_by_task_type:
            for node in self.nodes_and_tasks_by_task_type[task_type]:
                node.stop_running()
