from typing import Optional, Callable
from serial import Serial, SerialException
import asyncio
from serial_asyncio import SerialTransport
from sys import platform
from glob import glob
from threading import Thread

Port = Optional[int]
ROBOT_AUTO: Port = None


class Output(asyncio.Protocol):
    def __init__(self, *args):
        self.transport = None
        self.handler = None
        super().__init__(*args)

    def set_handler(self, handler: Optional[Callable]):
        self.handler = handler

    def connection_made(self, transport: SerialTransport):
        self.transport = transport

    def data_received(self, data):
        if self.handler is not None:
            self.handler(str(data, 'UTF-8'))

    def connection_lost(self, exc):
        raise RuntimeError('Connection with robot is lost.')


class Robot:
    AUTO = ROBOT_AUTO

    def __init__(self, port: Port = ROBOT_AUTO, read_handler: Optional[Callable] = None):
        self.loop = None
        self.robot_thread = None
        self.transport = None

        self.read_handler = read_handler

        self.MODE_FREE_DRIVE = 'mode_free'
        self.MODE_LINE_TASK = 'mode_line'
        self.MODE_MICRO_ROV = 'mode_micro'

        self.mode = self.MODE_FREE_DRIVE
        self.flags = []
        self.serial = self.create_serial(port)
        self.serial_buffer: str = ''
        assert self.serial is not None, "No compatible device is connected."

    def set_handler(self, read_handler):
        self.read_handler = read_handler

    def handle_read(self, data: str):
        rv = ''
        self.serial_buffer += data
        if '\n' in self.serial_buffer:
            arr = self.serial_buffer.splitlines()
            rv = arr.pop(0)
            self.serial_buffer = '\n'.join(arr)
        if self.read_handler is not None:
            self.read_handler(rv)

    async def create_serial_connection(self, loop, protocol: Output, serial: Serial):
        protocol.set_handler(self.handle_read)
        self.transport = SerialTransport(loop, protocol, serial)
        return self.transport, protocol

    def run(self):
        def thread_content(serial: Serial, creator: Callable):
            protocol = Output()
            try:
                asyncio.get_event_loop()
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())
            aio_loop = asyncio.get_event_loop()
            conn = creator(aio_loop, protocol, serial)
            aio_loop.run_until_complete(conn)
            aio_loop.run_forever()
        self.robot_thread = Thread(
            target=thread_content,
            args=(self.serial, self.create_serial_connection))
        self.robot_thread.daemon = False
        self.robot_thread.start()

    def close(self):
        pass

    def write(self, data: str):
        if not data.endswith('\n'):
            data = data + '\n'
        if self.serial is None:
            raise RuntimeError
        # print(f'writing {data} to serial')
        self.transport.write(bytes(data, 'UTF-8'))

    @staticmethod
    def create_serial(port: Port = ROBOT_AUTO, baud: int = 9600) -> Optional[Serial]:
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(255)]
            sole_port = 'COM%s' % port
        elif platform.startswith('linux') or platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob('/dev/tty[A-Za-z0-9]*')
            sole_port = '/dev/tty%s' % port
        elif platform.startswith('darwin'):
            ports = glob('/dev/tty.*')
            sole_port = '/dev/tty%s' % port
        else:
            raise EnvironmentError('Unsupported platform')

        if port is None:
            for port_instance in ports:
                try:
                    s = Serial(port_instance, baud, timeout=2, writeTimeout=0)
                    return s
                except (OSError, SerialException):
                    return None
        else:
            try:
                s = Serial(sole_port, baud, timeout=2, writeTimeout=0)
                return s
            except (OSError, SerialException) as e:
                raise e
