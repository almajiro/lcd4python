from copy import deepcopy

class Display:
    def __init__(self):
        self.buffer = [ [ 0x00 for _ in range(128)] for _ in range(64)]
        #self.render_buffer = [ 0x00 for _ in range(1024)]

    def set_buffer(self, new_buffer):
        self.buffer = new_buffer

    def render(self, device):
        render = 0
        for k in range(2):
            device.command(0x40, k)
            device.command(0xc0, k)

            for j in range(8):
                device.command(0xb8|j, k)

                for i in range(64):
                    if i == 0:
                        device.command(0x40, k)

                    display_data = 0x00

                    display_data |= (int(self.buffer[7+8*j][i+64*k]) & 0x01) << 7
                    display_data |= (int(self.buffer[6+8*j][i+64*k]) & 0x01) << 6
                    display_data |= (int(self.buffer[5+8*j][i+64*k]) & 0x01) << 5
                    display_data |= (int(self.buffer[4+8*j][i+64*k]) & 0x01) << 4
                    display_data |= (int(self.buffer[3+8*j][i+64*k]) & 0x01) << 3
                    display_data |= (int(self.buffer[2+8*j][i+64*k]) & 0x01) << 2
                    display_data |= (int(self.buffer[1+8*j][i+64*k]) & 0x01) << 1
                    display_data |= (int(self.buffer[0+8*j][i+64*k]) & 0x01)

                    display_data = ~display_data

                    display_data &= 0xFF

                    device.write(display_data, k)
