from typing import Callable
from WebServer import WebServer
from Actions import Actions, Robot
from atexit import register as register_exit_event
from ImageDetector import ImageDetector, cv2, Resolution
from threading import Thread
import time


def detector_loop(detector: ImageDetector, robot: Robot) -> Callable:
    def rv():
        time.sleep(2)
        movement = 'C'

        def do(m: str) -> str:
            detector.capture().detect_red_line().reset_bottom().detect_shapes().show()
            if robot.mode == robot.MODE_LINE_TASK:
                detector.find_direction()
                if m != detector.direction and m is not None:
                    robot.write(f'A\nD\nU\nJ\n{m}\n')
                    m = detector.direction
            detector.save()
            return m

        movement = do(movement)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if detector.IS_REAL_TIME or (cv2.waitKey(1) & 0xFF == ord('w')):
                movement = do(movement)
                if cv2.waitKey(1) & 0xFF == ord('w'):
                    time.sleep(0.020)
                continue
        detector.destroy()
    return rv


def main() -> int:
    server = WebServer(port=8085)  # Change this number to change the web server port being served.
    robot = Robot(port=None)  # Change this number to change the serial port number being used to control the robot.

    detector = ImageDetector(
        resolution_front=Resolution(1280, 720),
        resolution_bottom=Resolution(1280, 720),
        in_video_front='f.mp4',  # Set the in_video_front and in_video_bottom to 0 and 1 for cameras.
        in_video_bottom='b.mp4',
        # video_path_front=f'output_f_{time.time()}.avi',
        # video_path_bottom=f'output_b_{time.time()}.avi',
    )
    detector_thread = Thread(
        target=detector_loop(detector, robot))
    detector_thread.daemon = False
    detector_thread.start()

    actions = Actions(robot=robot, detector=detector)
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
