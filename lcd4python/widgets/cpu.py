from PIL import ImageDraw, ImageFont
import psutil

class Cpu:
    def __init__(self):
        self.name = 'CPU'
        self.fontBig = ImageFont.truetype('./lcd4python/fonts/k8x12L.ttf', 12)
        self.fontMid = ImageFont.truetype('./lcd4python/fonts/k8x12.ttf', 12)
        self.fontSm = ImageFont.truetype('./lcd4python/fonts/misaki_gothic_2nd.ttf', 8)
        self.fill = (0, 0, 0)

    # return img
    def render(self, image):
        draw = ImageDraw.Draw(image)

        mem = psutil.virtual_memory()

        cpu_util = psutil.cpu_percent(percpu=True)
        load_avg = psutil.getloadavg()

        for i in range(4):
            for j in range(4):
                draw.text((0+i*32, 0+j*10), '{:>3}'.format(str(int(cpu_util[j+i*4])) + '%'), fill=self.fill, font=self.fontSm)
                draw.rectangle([(0+i*32+13, 0+j*10), (0+i*32+30, 0+j*10+6)], fill=(255, 255, 255), outline=self.fill, width=1)

                bar = self.val_map(int(cpu_util[j+i*4]), 0, 100, 13, 30)
                draw.rectangle([(0+i*32+13, 0+j*10), (0+i*32+bar, 0+j*10+6)], fill=self.fill, width=1)


        draw.text((0, 41), 'Load Average:' + str(load_avg), fill=self.fill, font=self.fontSm)

        return image

    def sec_to_min(self, value):
        minute = 0
        while (value >= 60):
            value -= 60
            minute += 1
        return '{:02}'.format(minute) + ':' + '{:02}'.format(value)

    def val_map(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
