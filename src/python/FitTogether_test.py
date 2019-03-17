from WebServer import WebServer
from Actions import Actions, Robot
from atexit import register as register_exit_event


def main() -> int:
    server = WebServer(port=8085)
    robot = Robot(port=6)
    actions = Actions(robot=robot)
    robot.set_handler(actions.on_read)
    for name, action in actions.list.items():
        server.add_rule(name, action)
    server.run()
    actions.run()

    def on_exit():
        robot.close()
        server.close()

    register_exit_event(on_exit)
    return 0


if __name__ == "__main__":
    main()
