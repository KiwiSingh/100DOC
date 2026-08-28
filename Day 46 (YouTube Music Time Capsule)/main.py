#===========================================================IMPORTS========================================================================#

import requests
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic

#===========================================================CONSTANTS======================================================================#

BASE_URL = "https://web.archive.org/web/20141227151506/http://www.billboard.com:80/charts/hot-100/" # This base URL doesn't matter as much
                                                                                                    # since requests already handles 
                                                                                                    # redirects.
dates = input("When do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = BASE_URL + dates
PLAYLIST_NAME = f"{dates} Billboard 100"
playlist_id = None

#===========================================================SOUPY SOUP====================================================================#

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

try:
    response = requests.get(URL, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
except requests.RequestException as e:
    print(f"Error fetching the webpage: {e}")
title_divs = soup.find_all("div", class_="row-title")
song_titles = [
    div.find("h2").get_text(strip=True) for div in title_divs if div.find("h2") is not None
]
artist_titles = [
    div.find("h3").find("a").get_text(strip=True) for div in title_divs if div.find("h3") and div.find("h3").find("a") is not None
]
full_song_list = [                                                                              # This is done to improve the accuracy
                                                                                                # of YouTube Music's search
    f"{artist} - {song}"
    for artist, song in zip(artist_titles, song_titles)
]

#==========================================================YT MUSIC SHENANIGANS==========================================================#

yt = YTMusic("browser.json") 
playlists = yt.get_library_playlists(limit=100)
for p in playlists:
    if p["title"] == PLAYLIST_NAME:
        playlist_id = p["playlistId"]
        break

if playlist_id:
    print("This playlist already exists.")
else:
    playlist_id = yt.create_playlist(
        PLAYLIST_NAME,
        f"Playlist with the hottest songs from {dates}",
        privacy_status="PRIVATE",
    )
    print("Playlist created.")

for song in full_song_list:
    try:
        search_results = yt.search(song, filter="songs", limit=1)
        yt.add_playlist_items(playlist_id, [search_results[0]["videoId"]])
        print(f"Added: {song}")
    except Exception as e:
        print(f"Skipped: {song} | Reason: {e}")

print(f"Success! Enjoy the hottest hits from {dates}")
