import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Scope defines the level of access needed
scope = 'playlist-read-private playlist-read-collaborative user-library-read user-read-recently-played'

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    scope = scope,
    show_dialog = True))


def fetch_playlist_data(playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results1 = sp.playlist(playlist_id)
    results2 = sp.playlist_items(playlist_id)

    tracks = [{
        'name': item['track']['name'],
        'artists': item['track']['artists'],
        'artist': item['track']['artists'][0]['name'],
        'release_year': int(item['track']['album']['release_date'][:4]),
        'popularity': item['track']['popularity'],
        'album_img': item['track']['album']['images'][0]['url']  # Get the URL of the album artwork
    } for item in results2['items']]

    return {
        'name': results1['name'],
        'description': results1['description'],
        'tracks': tracks
    }


def fetch_recently_played():
    results = sp.current_user_recently_played(limit = 50)

    return results
