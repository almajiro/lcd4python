from serial import Serial

CONTROL_WORD = 0x04
WRITE_START_WORD = 0xE0
WRITE_END_WORD = 0xF0

class Device:
    def __init__(self, port, baudrate, display):
        self.port       = port
        self.baudrate   = baudrate
        self.display    = display

        try:
            self.device     = Serial(port, baudrate)
        except Exception as e:
            raise ConnectionError

    def display(self):
        return self.display

    def render(self):
        self.display.render(self)

    def close(self):
        self.device.close()

    def write(self, byte, cs):
        self.send(CONTROL_WORD | cs)
        self.send(WRITE_START_WORD)
        self.send(byte)
        self.send(WRITE_END_WORD)

    def command(self, byte, cs):
        self.send(CONTROL_WORD | 0x02 | cs)
        self.send(byte)

    def send(self, byte):
        self.device.write(bytes([byte]))

