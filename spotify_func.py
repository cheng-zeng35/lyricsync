# functions in this library are used to read information from Spotify

import os  # to set up Spotify environmental variables

import requests  # error catching
import spotipy  # Spotify API
from hanziconv import HanziConv  # used to convert Traditional Chinese names into Simplified Chinese
from spotipy.oauth2 import SpotifyOAuth  # Spotify API


# with a Spotify access token (sp), get information on the current song played and return a formatted version
def check_spotify(sp):
    try:
        current_track = sp.current_user_playing_track()
        return {'progress_ms': current_track['progress_ms'],
                'artist': current_track['item']['artists'][0]['name'],
                'length': current_track['item']['duration_ms'],
                'name': HanziConv.toSimplified(current_track['item']['name']),
                'playing': current_track['is_playing']}
    # TypeError when no music is being played on Spotify
    except TypeError or spotipy.exceptions.SpotifyException or requests.exceptions.ReadTimeout:
        return {'progress_ms': 0,
                'artist': 'N/A',
                'length': 0,
                'name': 'Nothing played right now or Spotify server error.',
                'playing': False}


# to get spotify access token based on credentials
# credentials is a dictionary with SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and USERNAME
def get_spotify_token(credentials):
    # update credentials
    for i in credentials:
        os.environ[i] = credentials[i]
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8080'

    # connect to API
    # return False if access failed
    try:
        scope = 'user-read-currently-playing'  # access scope, to add more scope, separate using space
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))  # access token
        _ = sp.current_user_playing_track()  # check if token is valid
        return sp
    except spotipy.exceptions.SpotifyException:
        return False
