from WebServer import WebServer
from Actions import Actions

def main() -> int:
    actions = None
    server = WebServer(port=8085)
    actions = Actions(port=3)
    for name, action in actions.list.items():
        server.add_rule(name, action)
    #try:
    server.run()
    while True:
        robot_out = actions.read_from_robot()
        print(robot_out)
        if len(robot_out):
            actions.buffer.append(robot_out)
    #except Exception:  # KeyboardInterrupt
    #    print('^C received, shutting down the program.')
    actions.serial.close()
        # server.close()
    return 0

if __name__ == "__main__":
    main()
