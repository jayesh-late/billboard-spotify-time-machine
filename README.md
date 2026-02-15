# Billboard to Spotify Time Machine

Scrapes Billboard Hot 100 chart from any date and automatically creates a Spotify playlist with those songs.

## Features

- Fetches Billboard Hot 100 chart for any specified date
- Searches for songs on Spotify
- Creates a private Spotify playlist with found tracks
- Handles songs that aren't available on Spotify

## Prerequisites

- Python 3.7+
- Spotify account
- Spotify Developer App credentials

## Setup

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in and create a new app
3. Note your **Client ID** and **Client Secret**
4. In app settings, add redirect URI: `http://localhost:8888/callback`

### 2. Set Environment Variables

**Windows (Command Prompt):**
```cmd
setx SPOTIPY_CLIENT_ID "your_client_id"
setx SPOTIPY_CLIENT_SECRET "your_client_secret"
setx SPOTIPY_REDIRECT_URI "http://localhost:8888/callback"
```

**Windows (PowerShell):**
```powershell
[System.Environment]::SetEnvironmentVariable('SPOTIPY_CLIENT_ID', 'your_client_id', 'User')
[System.Environment]::SetEnvironmentVariable('SPOTIPY_CLIENT_SECRET', 'your_client_secret', 'User')
[System.Environment]::SetEnvironmentVariable('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback', 'User')
```

**Linux/Mac:**
```bash
export SPOTIPY_CLIENT_ID='your_client_id'
export SPOTIPY_CLIENT_SECRET='your_client_secret'
export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

Enter a date in `YYYY-MM-DD` format when prompted (e.g., `2000-08-12`).

The script will:
1. Scrape the Billboard Hot 100 for that date
2. Search for each song on Spotify
3. Create a private playlist named "[DATE] Billboard 100"
4. Add all found tracks to the playlist

## Example
```
Which year do you want to travel to? Type the date in this format YYYY-MM-DD: 2010-07-15
```

Output:
```
Playlist '2010-07-15 Billboard 100' created successfully with 95 songs!
```

## Notes

- Some songs may not be available on Spotify and will be skipped
- First run will open a browser for Spotify authentication
- Authentication token is cached in `.cache` file (not tracked in git)

## Tech Stack

- Python 3
- BeautifulSoup4 - Web scraping
- Spotipy - Spotify API wrapper
- Requests - HTTP library

## License

MIT
