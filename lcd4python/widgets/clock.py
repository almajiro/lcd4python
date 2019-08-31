from datetime import datetime
from PIL import ImageDraw, ImageFont

class Clock:
    def __init__(self):
        self.name = 'CLOCK'
        self.fontBig = ImageFont.truetype('/home/almajiro/.local/share/fonts/ProFont For Powerline.ttf', 30)
        self.fontMid = ImageFont.truetype('/home/almajiro/.local/share/fonts/ProFont For Powerline.ttf', 16)
        self.fill = (0, 0, 0)

        self.weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def render(self, image):
        draw = ImageDraw.Draw(image)

        now = datetime.now()
        draw.text((5, 0), now.strftime('%H:%M:%S'), fill=self.fill, font=self.fontBig)
        draw.text((5, 25), now.strftime('%Y/%m/%d'), fill=self.fill, font=self.fontMid)
        draw.text((5, 38), self.weekday[now.weekday()], fill=self.fill, font=self.fontMid)

        return image
