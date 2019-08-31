from PIL import ImageDraw, ImageFont, Image
import subprocess
import json

DEFAULT_ATTRIBUTES = (
    'index',
    'uuid',
    'name',
    'timestamp',
    'memory.total',
    'memory.free',
    'memory.used',
    'utilization.gpu',
    'utilization.memory'
)

class Nvidia:
    def __init__(self):
        self.name = 'NVIDIA'
        self.fontBig = ImageFont.truetype('./lcd4python/fonts/k8x12L.ttf', 12)
        self.fontMid = ImageFont.truetype('./lcd4python/fonts/k8x12.ttf', 12)
        self.fontSm = ImageFont.truetype('./lcd4python/fonts/misaki_gothic_2nd.ttf', 8)
        self.fill = (0, 0, 0)

        self.nvidia_img = Image.open('./lcd4python/images/nvidia.jpg')

    def render(self, image):
        draw = ImageDraw.Draw(image)

        image.paste(self.nvidia_img.resize((40, 40), Image.ANTIALIAS), (0, 5))

        gpu_info = self.get_gpu_info()
        gpu_name = gpu_info[0]['name']
        gpu_mem_total = gpu_info[0]['memory.total']
        gpu_mem_free = gpu_info[0]['memory.free']
        gpu_mem_used = gpu_info[0]['memory.used']

        draw.text((42, 0), gpu_name, fill=self.fill, font=self.fontSm)
        draw.text((42, 9), 'Mem Total : ' + gpu_mem_total + ' MB', fill=self.fill, font=self.fontSm)
        draw.text((42, 18), 'Mem Free  : ' + gpu_mem_free + ' MB', fill=self.fill, font=self.fontSm)
        draw.text((42, 27), 'Mem Used  : ' + gpu_mem_used + ' MB', fill=self.fill, font=self.fontSm)

        draw.rectangle([(42, 40), (100, 48)], outline=self.fill, fill=(255, 255, 255), width=1)

        mem_bar_percentage = self.val_map(int(gpu_mem_used), 0, int(gpu_mem_total), 42, 100)
        draw.rectangle([(42, 40), (mem_bar_percentage, 48)], fill=self.fill)

        mem_percentage = self.val_map(int(gpu_mem_used), 0, int(gpu_mem_total), 0, 100)
        draw.text((110, 41), str(int(mem_percentage)) + '%', fill=self.fill, font=self.fontSm)

        return image

    def get_gpu_info(self, nvidia_smi_path='nvidia-smi', keys=DEFAULT_ATTRIBUTES, no_units=True):
        nu_opt = '' if not no_units else ',nounits'
        cmd = '%s --query-gpu=%s --format=csv,noheader%s' % (nvidia_smi_path, ','.join(keys), nu_opt)
        output = subprocess.check_output(cmd, shell=True)
        lines = output.decode().split('\n')
        lines = [ line.strip() for line in lines if line.strip() != '' ]
    
        return [ { k: v for k, v in zip(keys, line.split(', ')) } for line in lines ]

    def val_map(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
