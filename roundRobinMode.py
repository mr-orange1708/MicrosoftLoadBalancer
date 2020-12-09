from runtimeMode import RuntimeMode


class RoundRobinMode(RuntimeMode):
    def __init__(self, node_and_task_container: dict) -> None:
        super().__init__(node_and_task_container)
        self.prev_node_by_task_type = {}

        for task_type in node_and_task_container:
            self.prev_node_by_task_type[task_type] = -1
    
    def get_node_position_by_task_type(self, task_type: str) -> int:
        return self.find_next_node_by_order(task_type)

    def find_next_node_by_order(self, task_type: str) -> int:
        current_node_by_task_type = self.prev_node_by_task_type[task_type] + 1

        if current_node_by_task_type == len(self.node_and_task_container[task_type]):
            current_node_by_task_type = 0

        self.prev_node_by_task_type[task_type] = current_node_by_task_type

        return current_node_by_task_type
