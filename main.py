import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import re

# Prompt user for the date they want to travel back to
date =  input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Construct Billboard Hot 100 URL for the specified date
URL = "https://www.billboard.com/charts/hot-100/" + date

# Set headers to mimic a real browser request (avoids blocking)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# Fetch the Billboard chart page
response = requests.get(URL,headers=headers)

# Parse HTML content with BeautifulSoup
html_code = response.text
soup = BeautifulSoup(html_code,"html.parser")

# Print the page title to confirm successful scrape
print(soup.title)

# Extract all song titles from the Hot 100 chart
# Billboard uses specific CSS classes for song entries
Top_100_songs = soup.select(".o-chart-results-list__item h3")

# Clean up song titles and store in a list
top_songs = []
for Top_song_titles in Top_100_songs:
    # Remove leading/trailing whitespace and newlines
    top_songs.append(Top_song_titles.get_text(strip=True))

# Display extracted songs for verification
print(top_songs)

# Initialize Spotify API client with OAuth authentication
# Credentials are read from environment variables:
# - SPOTIPY_CLIENT_ID
# - SPOTIPY_CLIENT_SECRET
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="https://example.org/callback",
        scope="playlist-modify-private"
    )
)

# Get the authenticated user's Spotify ID
user = sp.current_user()
print("Logged in as:", user["id"])

# Search for each song on Spotify and collect track URIs
song_uris = []
year = date.split("-")[0] # Extract year from date for more accurate search



def clean_song_title(title):
    return re.sub(r"\(.*?\)", "", title).strip()


for song in top_songs:
    clean_title = clean_song_title(song)

    # Query Spotify API with song name and year
    result = sp.search(
        q=f"track:{clean_title}",
        type="track",
        limit=1
    )

    try:
        # Extract the Spotify URI for the first matching track
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        # Song not found on Spotify - skip it
        print(f"❌ Song not found on Spotify: {clean_title}")


# Create a new private playlist for the Billboard chart
playlist = sp.user_playlist_create(
    user=sp.current_user()["id"],
    name=f"{date} Billboard 100", # Playlist name includes the date
    public=False,  # Keep playlist private
    description="Time machine playlist"
)

# Add all found tracks to the newly created playlist
sp.playlist_add_items(playlist["id"], song_uris)
