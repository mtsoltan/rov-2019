from typing import Callable

from ImageDetector import ImageDetector
from Robot import Robot
from WebServer import Response
import asyncio
import websockets
from threading import Thread


class Actions:
    def __init__(self, robot: Robot, detector: ImageDetector, ws_url: str = 'localhost', ws_port: int = 8123):
        self.url = ws_url
        self.port = ws_port

        self.server = None
        self.server_thread = None
        self.rules = {}

        self.robot = robot
        self.detector = detector
        self.buffer = []
        self.VALID_CODES = [
            'M',  # Metal
            'E',  # Error
        ]
        self.FLAG_BEGIN_SHAPE_TASK = 'shape_task'
        self.FLAG_BEGIN_CANNON_TASK_S = 'cannon_task_s'
        self.FLAG_BEGIN_CANNON_TASK_F = 'cannon_task_f'
        self.FLAG_BEGIN_CANNON_TASK_B = 'cannon_task_b'
        self.ACTION_MOVE_FREE_DRIVE = 'move_free_drive'
        self.ACTION_FLUSH_BUFFER = 'flush_buffer'
        self.ACTION_GET_MODE = 'get_mode'
        self.list = {
            self.robot.MODE_FREE_DRIVE: self.enable_free_drive,
            self.robot.MODE_LINE_TASK: self.enable_line_task,
            self.robot.MODE_MICRO_ROV: self.enable_micro_rov,
            self.FLAG_BEGIN_SHAPE_TASK: self.print_shape_task,
            self.FLAG_BEGIN_CANNON_TASK_S: self.print_cannon_task_s,
            self.FLAG_BEGIN_CANNON_TASK_F: self.print_cannon_task_f,
            self.FLAG_BEGIN_CANNON_TASK_B: self.print_cannon_task_b,
            self.ACTION_MOVE_FREE_DRIVE: self.move_free_drive,
            self.ACTION_FLUSH_BUFFER: self.flush_buffer,
            self.ACTION_GET_MODE: self.get_mode,
        }

    def run(self):
        def thread_content(url: str, port: int, on_data: Callable):
            try:
                asyncio.get_event_loop()
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())
            aio_loop = asyncio.get_event_loop()
            aio_loop.run_until_complete(
                websockets.serve(on_data, url, port))
            aio_loop.run_forever()
        self.server_thread = Thread(
            target=thread_content,
            args=(self.url, self.port, self.handle_ws_request,))
        self.server_thread.daemon = False
        self.server_thread.start()
        self.robot.run()

    def close(self):
        pass

    def print_shape_task(self, _: str) -> Response:
        return (f'\n'
                f'triangle        {self.detector.triangle_count}\n'
                f'big_rectangle   {self.detector.big_rectangle_count}\n'
                f'small_rectangle {self.detector.small_rectangle_count}\n'
                f'circle          {self.detector.circle_count}\n')

    def print_cannon_task_s(self, _: str) -> Response:
        print(self.FLAG_BEGIN_CANNON_TASK_S)
        return "Cannon Dummy"

    def print_cannon_task_f(self, _: str) -> Response:
        print(self.FLAG_BEGIN_CANNON_TASK_S)
        return "Cannon Dummy"

    def print_cannon_task_b(self, _: str) -> Response:
        print(self.FLAG_BEGIN_CANNON_TASK_S)
        return "Cannon Dummy"

    def enable_free_drive(self, _: str) -> Response:
        self.robot.mode = self.robot.MODE_FREE_DRIVE
        return 'Free drive enabled.'

    def enable_line_task(self, _: str) -> Response:
        self.detector.reset_front()
        self.robot.mode = self.robot.MODE_LINE_TASK
        return 'Line following task enabled.'

    def enable_micro_rov(self, _: str) -> Response:
        self.robot.mode = self.robot.MODE_MICRO_ROV
        return 'Line following task enabled.'

    def move_free_drive(self, body: str) -> Response:
        if self.robot.mode != self.robot.MODE_FREE_DRIVE:  # TODO: Add micro-rov support.
            return 400, 'Attempted to move the robot while not in free drive.'
        if len(body) > 50:
            return 400, 'Only simple commands are allowed to be sent, one at a time.'
        self.send_to_robot(body)
        return 'Requested that robot does the action defined by the letter %s.' % body

    def flush_buffer(self, _: str) -> Response:
        temp = '\n'.join(self.buffer)
        self.buffer = []
        for l in self.VALID_CODES:
            if temp.startswith(l):
                return temp
        return temp and 'F' + temp or temp

    async def handle_ws_request(self, websocket, _):
        async for _ in websocket:
            temp = '\n'.join(self.buffer)
            self.buffer = []
            await websocket.send(temp)

    def get_mode(self, _: str) -> Response:
        return self.robot.mode

    def send_to_robot(self, body):
        try:
            self.robot.write(body)
        except RuntimeError:
            if 'ESerialError' not in self.buffer:
                self.buffer.append('ESerialError')

    def on_read(self, data):
        if len(data):
            # print('SERIAL READ: ' + data)
            self.buffer.append(data)
