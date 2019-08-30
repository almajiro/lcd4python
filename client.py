from PIL import Image, ImageDraw, ImageFont
from mpd import MPDClient
from datetime import datetime
import numpy as np
import time
import socket
from device import Device
from display import Display

from widget_cpu import Widget_Cpu
from widget_gpu import Widget_Gpu
from widget_clock import Widget_Clock
from widget_mpd import Widget_Mpd
from widget_linux import Widget_Linux

def status_line(img, name):
    draw = ImageDraw.Draw(img)
    
    now = datetime.now()

    draw.rectangle(((0,53), (127, 63)), fill=fill)
    draw.text((90, 55), name, fill=(255, 255, 255), font=font)
    draw.text((2, 55), now.strftime("%Y/%m/%d %H:%M:%S"), fill=(255, 255, 255), font=font)

    return img

def img_to_bmp(img):
    ary = np.array(img)

    # Split the three channels
    r,g,b = np.split(ary,3,axis=2)
    r = r.reshape(-1)
    g = r.reshape(-1)
    b = r.reshape(-1)

    # Standard RGB to grayscale 
    bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2], zip(r,g,b)))
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap > 128).astype(float),255)

    return bitmap

def splashscreen():
    img = Image.new('RGB', (128,64), (255, 255, 255))
    arch_img = Image.open('./images/archlinux.png')

    img.paste(arch_img.resize((64, 64)), (30, 0))

    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 48), (128, 60)), fill=fill)
    draw.text((34, 49), 'lcd4python', fill=(255, 255, 255))

    device.display.set_buffer(img_to_bmp(img))
    device.render()

    time.sleep(2)

fill = (0, 0, 0)
font = ImageFont.truetype('./fonts/misaki_gothic_2nd.ttf', 8)

device = Device('/dev/ttyACM0', 9600, Display())
splashscreen()

widgets = [
    [
        Widget_Linux(),
        5,
        0
    ],
    [
        Widget_Gpu(),
        5,
        0
    ],
    [
        Widget_Cpu(),
        10,
        0
    ],
    [
        Widget_Clock(),
        5,              # display time
        0,              # start display time
    ],
    [
        Widget_Mpd(),
        30,
        0
    ]
]

index = 0

while True:
    for widget in widgets:
        while True:
            image = Image.new('RGB', (128, 64), (255, 255, 255))

            device.display.set_buffer(img_to_bmp(status_line(widget[0].render(image), widget[0].name)))
            device.render()

            if widget[2] == 0:
                widget[2] = time.time()

            if ((time.time() - widget[2]) > widget[1]):
                widget[2] = 0
                break

device.close()
