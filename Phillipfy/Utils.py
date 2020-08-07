import colorgram
import requests


class Utils():
    def __init__(self):
        pass

    def hex_to_xy(self, hex):
        R = int(hex[:2], 16)
        G = int(hex[2:4], 16)
        B = int(hex[4:6], 16)

        total = R + G + B

        if R == 0:
            firstPos = 0
        else:
            firstPos = R / total

        if G == 0:
            secondPos = 0
        else:
            secondPos = G / total

        return [firstPos, secondPos]

    def rgb_to_xy(self, R, G, B):
        total = R + G + B

        if R == 0:
            firstPos = 0
        else:
            firstPos = R / total

        if G == 0:
            secondPos = 0
        else:
            secondPos = G / total

        return [firstPos, secondPos]

    def extract_colors(self, url, n=4):
        img = requests.get(url)
        return colorgram.extract(img.content, 4)
