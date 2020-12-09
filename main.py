import argparse
from loadBalancer import LoadBalancer


def main():
    nodeFilePath = None
    taskFilePath = None

    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes_config_path", "-ncp", help = "set the nodes configuration file path")
    parser.add_argument("--tasks_config_path", "-tcp", help = "set the tasks configuration file path")
    args = parser.parse_args()

    if args.nodes_config_path:
        nodeFilePath = args.nodes_config_path
    else:
        print ("Missing nodes configuration file path")
        return

    if args.tasks_config_path:
        taskFilePath = args.tasks_config_path
    else:
        print ("Missing tasks configuration file path")
        return

#    nodeFilePath = "c:\\Users\\טל\\Desktop\\MicrosoftLoadBalancer\\nodesConfig.json"
#    taskFilePath = "c:\\Users\\טל\\Desktop\\MicrosoftLoadBalancer\\tasksConfig.txt"


    loadBalancer = LoadBalancer()
    retValue, retMessage = loadBalancer.read_nodes_from_file(nodeFilePath)

    if retValue == False:
        print (retMessage)
        return

    retValue, retMessage = loadBalancer.read_tasks_from_file(taskFilePath)

    if retValue == False:
        print (retMessage)
        return

    loadBalancer.stop_running()


if __name__=='__main__':
    main()