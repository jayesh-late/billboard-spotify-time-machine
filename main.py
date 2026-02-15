import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import re

date =  input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = "https://www.billboard.com/charts/hot-100/" + date

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

response = requests.get(URL,headers=headers)

html_code = response.text
soup = BeautifulSoup(html_code,"html.parser")
print(soup.title)

Top_100_songs = soup.select(".o-chart-results-list__item h3")

top_songs = []
for Top_song_titles in Top_100_songs:
    top_songs.append(Top_song_titles.get_text(strip=True))
print(top_songs)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="https://example.org/callback",
        scope="playlist-modify-private"
    )
)

user = sp.current_user()
print("Logged in as:", user["id"])

song_uris = []
year = date.split("-")[0]



def clean_song_title(title):
    return re.sub(r"\(.*?\)", "", title).strip()


for song in top_songs:
    clean_title = clean_song_title(song)

    result = sp.search(
        q=f"track:{clean_title}",
        type="track",
        limit=1
    )

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"❌ Song not found on Spotify: {clean_title}")


playlist = sp.user_playlist_create(
    user=sp.current_user()["id"],
    name=f"{date} Billboard 100",
    public=False,
    description="Time machine playlist"
)

sp.playlist_add_items(playlist["id"], song_uris)
