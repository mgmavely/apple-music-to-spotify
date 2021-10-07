from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# inp = input("Which year do you want to travel to?  Type the date in this format YYYY-MM-DD:\n")

response = requests.get("https://music.apple.com/us/playlist/study-beats/pl.a4e197979fc74b2a91b3cdf869f12aa5")
response.raise_for_status()
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

playlist_info = soup.find_all(name="div", class_="songs-list-row__song-name-wrapper")
song_names = [i.text.split('\n')[1] for i in playlist_info]
song_artists = [i.text.split('\n')[5] for i in playlist_info]
# print(song_artists)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
    client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
    show_dialog=True,
    cache_path="token.txt"

))
# print("OK?")
spotify_songs = []
for i in range(len(song_artists)):
    item = sp.search(q=f"track:{song_names[i]} artist:{song_artists[i]}", limit=1)
    try:
        spotify_songs.append(item['tracks']['items'][-1]['external_urls']['spotify'])
    except IndexError:
        pass

user_id = sp.current_user()['id']

playlist = sp.user_playlist_create(user=user_id, name=f"Apple Music -> Spotify",
                                   public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=spotify_songs)
