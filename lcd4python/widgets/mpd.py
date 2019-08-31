from PIL import ImageDraw, ImageFont
from mpd import MPDClient

class Mpd:
    def __init__(self):
        self.name = 'MPD'
        self.fontBig = ImageFont.truetype('./lcd4python/fonts/k8x12L.ttf', 12)
        self.fontMid = ImageFont.truetype('./lcd4python/fonts/k8x12.ttf', 12)
        self.fontSm = ImageFont.truetype('./lcd4python/fonts/misaki_gothic_2nd.ttf', 8)
        self.fill = (0, 0, 0)

        self.mpd = MPDClient()
        self.mpd.connect('localhost', 6600)

    # return img
    def render(self, image):
        draw = ImageDraw.Draw(image)

        status = self.mpd.status()
        song = self.mpd.currentsong()

        time = status['time'].split(":")
        time_label = self.sec_to_min(int(time[0])) + '/' + self.sec_to_min(int(time[1])) + ' | ' + status['bitrate'] + 'kbps' + ' | ' + status['volume'] + '%'

        draw.text((0, 0), song['title'], fill=self.fill, font=self.fontMid)
        draw.text((0, 12), song['artist'], fill=self.fill, font=self.fontMid)
        draw.text((0, 24), song['album'], fill=self.fill, font=self.fontMid)

        line = self.val_map(int(time[0]), 0, int(time[1]), 0, 128)
        draw.line([(0, 36), (line, 36)], fill=self.fill)
        draw.rectangle(((line, 35), (line+2), 37), fill=self.fill)

        draw.text((0, 38), time_label, fill=self.fill, font=self.fontBig)

        return image

    def sec_to_min(self, value):
        minute = 0
        while (value >= 60):
            value -= 60
            minute += 1
        return '{:02}'.format(minute) + ':' + '{:02}'.format(value)

    def val_map(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
