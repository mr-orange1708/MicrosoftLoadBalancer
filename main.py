import argparse
from loadBalancer import LoadBalancer


def main():
    node_file_path = None
    task_file_path = None
    runtime_mode_file_path = None

    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes_config_path", "-ncp", help = "set the nodes configuration file path")
    parser.add_argument("--tasks_config_path", "-tcp", help = "set the tasks configuration file path")
    parser.add_argument("--runtime_mode_file_path", "-rmfp", help = "external file for runtime mode")
    args = parser.parse_args()

    if args.nodes_config_path:
        node_file_path = args.nodes_config_path
    else:
        print("Missing nodes configuration file path")
        return

    if args.tasks_config_path:
        task_file_path = args.tasks_config_path
    else:
        print("Missing tasks configuration file path")
        return

    if args.runtime_mode_file_path:
        runtime_mode_file_path = args.runtime_mode_file_path
    else:
        print("Missing external runtime mode file path")
        return

    load_balancer = LoadBalancer()
    ret_value, ret_message = load_balancer.read_nodes_from_file(node_file_path)

    if ret_value == False:
        print(ret_message)
        load_balancer.stop_running()
        return

    ret_value, ret_message = load_balancer.read_tasks_from_file(task_file_path, runtime_mode_file_path)

    if ret_value == False:
        print(ret_message)

    load_balancer.stop_running()


if __name__=='__main__':
    main()