from PIL import ImageDraw, ImageFont, Image
import netifaces
import subprocess
import json
import time

PACMAN_CHECK_INTERVAL = 1800

class Widget_Linux:
    def __init__(self):
        self.name = 'LINUX'
        self.fontBig = ImageFont.truetype('./fonts/k8x12L.ttf', 12)
        self.fontMid = ImageFont.truetype('./fonts/k8x12.ttf', 12)
        self.fontSm = ImageFont.truetype('./fonts/misaki_gothic_2nd.ttf', 8)
        self.fill = (0, 0, 0)

        self.nodename = subprocess.check_output(['uname', '-n']).decode()
        self.kernel_release = subprocess.check_output(['uname', '-r']).decode()
        self.updates = []

        self.ip = netifaces.ifaddresses('eno1')[netifaces.AF_INET][0]['addr']

        self.prev_update_time = 0

        self.distro_img = Image.open('./images/archlinux-logo.png')

    def render(self, image):
        draw = ImageDraw.Draw(image)

        image.paste(self.distro_img.resize((40, 40), Image.ANTIALIAS), (0, 0))

        if (self.prev_update_time == 0 or (self.prev_update_time - time.time()) > PACMAN_CHECK_INTERVAL):
            self.prev_update_time = time.time()
            self.check_updates()

        draw.text((45, 0), self.nodename, fill=self.fill, font=self.fontSm)
        draw.text((45, 9), self.kernel_release, fill=self.fill, font=self.fontSm)
        draw.text((45, 18), self.ip, fill=self.fill, font=self.fontSm)

        if len(self.updates):
            update_msg = str(len(self.updates)) + ' package needs to update'
        else:
            update_msg = 'No updates available.'

        draw.text((0, 43), update_msg, fill=self.fill, font=self.fontSm)

        return image

    def check_updates(self):
        print("get updates")
        updates = subprocess.check_output(['checkupdates']).decode()
        self.updates = updates.split("\n")

    def val_map(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
