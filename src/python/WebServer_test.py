from WebServer import WebServer


def task1() -> str:
    # Task one happens here.
    return 'task 1 response'


def main() -> int:
    server = WebServer(port=8085)
    server.add_rule('task1', task1)
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()
        return 0


if __name__ == "__main__":
    main()
