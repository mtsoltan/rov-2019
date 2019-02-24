from serial import Serial, SerialException


class Actions:
    def __init__(self, port: int = 0):
        self.MODE_FREE_DRIVE = 'mode_free'
        self.MODE_LINE_TASK = 'mode_line'
        self.MODE_MICRO_ROV = 'mode_micro'
        self.FLAG_IN_SHAPE_TASK = 'move_free_drive'
        self.ACTION_FLUSH_BUFFER = 'flush_buffer'
        self.ACTION_GET_MODE = 'get_mode'

        self.mode = self.MODE_FREE_DRIVE
        self.flags = []
        self.buffer = []
        self.list = {
            self.MODE_FREE_DRIVE: self.enable_free_drive,
            self.MODE_LINE_TASK: self.enable_line_task,
            self.MODE_MICRO_ROV: self.enable_micro_rov,
            self.FLAG_IN_SHAPE_TASK: self.move_free_drive,
            self.ACTION_FLUSH_BUFFER: self.flush_buffer,
            self.ACTION_GET_MODE: self.get_mode,
        }

        try:
            self.serial = Serial(f'COM{port}', 9600, timeout=2, writeTimeout=0)
        except SerialException:
            raise RuntimeError(f'Could not open the serial port {port}.')

    def enable_free_drive(self, body: str) -> str:
        self.mode = self.MODE_FREE_DRIVE
        return 'Free drive enabled.'

    def enable_line_task(self, body: str) -> str:
        self.mode = self.MODE_LINE_TASK
        return 'Line following task enabled.'

    def enable_micro_rov(self, body: str) -> str:
        self.mode = self.MODE_MICRO_ROV
        return 'Line following task enabled.'

    def move_free_drive(self, body: str):
        if self.mode != self.MODE_FREE_DRIVE:  # TODO: Add micro-rov support.
            return 400, 'Attempted to move the robot while not in free drive.'
        if len(body) != 1:
            return 400, 'Body needs to only be a single letter for free drive.'
        self.send_to_robot(body+'\n')
        return 'Requested that robot does the action defined by the letter %s.' % body

    def flush_buffer(self, body: str):
        temp = '\n'.join(self.buffer)
        self.buffer = []
        return temp

    def get_mode(self, body: str):
        return self.mode

    def send_to_robot(self, body):
        if self.serial is None or not self.serial.is_open:
            if 'SerialError' not in self.buffer:
                self.buffer.append('ESerialError')
            return
        self.serial.write(bytes(body, 'UTF-8'))

    def read_from_robot(self):
        rv = ''
        if self.serial is None or not self.serial.is_open:
            if 'SerialError' not in self.buffer:
                self.buffer.append('ESerialError')
            return rv
        # self.serial.in_waiting
        try:
            rv = self.serial.readline().decode('UTF-8').replace('\n', '')
        except Exception:
            rv = ''
        return rv
