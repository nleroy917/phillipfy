import phue
from phue import Bridge
import requests
import time
import sys

from .Utils import Utils
from .Spotify import Spotify

util = Utils()


class Phillipfy():
    '''
    Phillipfy application - call run() to start
    '''

    def __init__(self, room=None):
        '''
        This method is called when an instance of the Phillipfy class is
        created
            :param - room - select the room you want to run the app in.
            Default is None, which will subsequently default to the first
            group.
        '''

        # Get the local ip o fthe bridge and init a Bridge class
        IP_URL = 'https://discovery.meethue.com/'
        res = requests.get(IP_URL)
        ip_data = res.json()[0]
        self._ID = ip_data['id']
        self._INTERNALIP = ip_data['internalipaddress']
        try:
            self._bridge = Bridge(self._INTERNALIP)
        except phue.PhueRegistrationException:
            print('''Error! The link button probably hasnt been pressed on your
            Hue Bridge. Do this and start the app within 30 seconds - it only
            needs to be done once!''')
            sys.exit(1)

        # init helper objects and connect to bridge
        self._bridge.connect()
        self._util = Utils()
        self._sp = Spotify()
        self._groups = self._bridge.get_group()
        self._room = room

        # extract group number from room name
        if self._room is None:
            self._group = 1  # get default if not specified
        else:
            self._group = int(self._get_group_from_room(self._room))

        # get light ids to interact with
        self._lights = [
            int(x) for x in self._bridge.get_group(
                self._group)['lights']]

        # init current song + color states
        self._current_song = self._sp.current_song()
        if self._current_song is None:
            print('Please start playing Spotify first!')
            sys.exit(1)
        self._current_id = self._current_song['item']['id']

        print('Starting Phillipfy for {} (Group - {})'.format(
            self._room, self._group))
        print('Using lights {}'.format(self._lights))
        song = self._get_song_name(self._current_song)
        artist = self._get_artist(self._current_song)
        print('Now playing - {}, {}'.format(song, artist))
        colors = self._util.extract_colors(
            self._current_song['item']['album']['images'][0]['url'])
        self._set_colors(colors)

    def _get_group_from_room(self, room):
        '''
        Search thru the available groups and look for one with
        a name that matches the one the app was init with
        '''
        for group_num in self._groups:
            if self._groups[group_num]['name'].lower() == room.lower():
                return group_num
        return 1

    def _get_current_song(self):
        '''
        Interface my Spotify class to get the current song playing
        '''
        return self._sp.current_song()

    def _get_song_name(self, song):
        '''
        Extract the song name from the song object returned from spotify
        '''
        return song['item']['name']

    def _get_artist(self, song):
        '''
        Extract the song artist form the song object returned from spotify
        '''
        return song['item']['artists'][0]['name']

    def _extract_colors(self, current_song):
        url = current_song['item']['album']['images'][0]['url']
        return self._util.extract_colors(url, n=len(self._lights))

    def _set_colors(self, colors):
        '''
        Set the colors for the lights
            :param - colors - a list (or tuple) of rgb tuples. Must be
            the same length as the number of lights in the room
        '''
        if len(self._lights) != len(colors):
            print(
                '''Error! Color list must be same length as number of
                lights in the room!''')

        print('Changing colors ... ')
        for light_id, color in zip(self._lights, colors):
            self._bridge.set_light(
                light_id, 'xy', self._util.rgb_to_xy(
                    color.rgb.r, color.rgb.g, color.rgb.b))

    def run(self):
        try:
            while True:
                self._current_song = self._get_current_song()
                if self._current_song['item']['id'] == self._current_id:
                    pass
                    time.sleep(3)
                else:
                    self._current_id = self._current_song['item']['id']
                    song = self._get_song_name(self._current_song)
                    artist = self._get_artist(self._current_song)
                    print('Now playing - {}, {}'.format(song, artist))
                    colors = self._extract_colors(self._current_song)
                    self._set_colors(colors)

        except KeyboardInterrupt:
            print('Shutting down ...')
            sys.exit(0)
