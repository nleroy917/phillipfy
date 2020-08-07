import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

class Spotify():
    '''
    Python class to interface the Spotify API - requires implicit grant flow
    '''
    def __init__(self):
        load_dotenv()
        self._scopes = 'user-read-currently-playing user-read-playback-state'
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self._scopes))
    
    def current_song(self):
        return self._sp.current_playback()
