from phue import Bridge
import requests
import time
import sys

from .Utils import Utils
from .Spotify import Spotify

util = Utils()

class Phillipfy():
    def __init__(self,room=None):

        IP_URL = 'https://discovery.meethue.com/'
        res = requests.get(IP_URL)
        ip_data = res.json()[0]

        self._ID = ip_data['id']
        self._INTERNALIP = ip_data['internalipaddress']
        self._bridge = Bridge(self._INTERNALIP)

        self._bridge.connect()
        self._util = Utils()
        self._sp = Spotify()
    
    def _get_current_song(self):
        return self._sp.current_song()
    
    def run(self):
        try:
            current_song = self._get_current_song()
            stored_id = current_song['item']['id']
            colors = self._util.extract_colors(current_song['item']['album']['images'][0]['url'])
            print('Colors Extracted.')
            color1 = self._util.rgb_to_xy(colors[0].rgb.r, colors[0].rgb.g, colors[0].rgb.b)
            color2 = self._util.rgb_to_xy(colors[1].rgb.r, colors[1].rgb.g, colors[1].rgb.b)
            color3 = self._util.rgb_to_xy(colors[2].rgb.r, colors[2].rgb.g, colors[2].rgb.b)
            color4 = self._util.rgb_to_xy(colors[3].rgb.r, colors[3].rgb.g, colors[3].rgb.b)
            self._bridge.set_light(1,'xy',color1)
            self._bridge.set_light(1,'xy',color2)
            self._bridge.set_light(1,'xy',color3)
            self._bridge.set_light(1,'xy',color4)
            print('Color set!')

            while True:
                current_song = self._get_current_song()
                print('Current Song:\t{}\t{}'.format(current_song['item']['name'],current_song['item']['artists'][0]['name']))
                fetched_id = current_song['item']['id']

                if fetched_id != stored_id:
                    colors = self._util.extract_colors(current_song['item']['album']['images'][0]['url'])
                    print('Colors Extracted.')
                    color1 = self._util.rgb_to_xy(colors[0].rgb.r, colors[0].rgb.g, colors[0].rgb.b)
                    color2 = self._util.rgb_to_xy(colors[1].rgb.r, colors[1].rgb.g, colors[1].rgb.b)
                    color3 = self._util.rgb_to_xy(colors[2].rgb.r, colors[2].rgb.g, colors[2].rgb.b)
                    color4 = self._util.rgb_to_xy(colors[3].rgb.r, colors[3].rgb.g, colors[3].rgb.b)
                    self._bridge.set_light(1,'xy',color1)
                    self._bridge.set_light(2,'xy',color2)
                    self._bridge.set_light(3,'xy',color3)
                    self._bridge.set_light(4,'xy',color4)
                    print('Color set!')
                    stored_id = fetched_id
                else: 
                    print('No song change detected.')

                time.sleep(3)
        except KeyboardInterrupt:
            print('Shutting down ...')
            sys.exit(0)

