import requests
from bs4 import BeautifulSoup

URL = "https://www.empireonline.com/movies/features/best-movies-2/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}
response = requests.get(URL, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, "html.parser")
movie_titles = [title.get_text(strip=True) for title in soup.select("h2:has(strong)")][::-1]
movie_titles.pop()
junk = {"10 — 1", "25 — 11", "50 — 26", "75 — 51"}
movie_titles = [m for m in movie_titles if m not in junk]
new_movie_titles = []
for movie in movie_titles:
    movie_name = movie.split(") ")[1]
    movie_rank = movie.split(") ")[0]
    new_movie_titles.append(f"{movie_rank}. {movie_name}")
with open("top_100_movies.txt", "w", encoding="utf-8") as f:
    for title in new_movie_titles:
        f.write(title + "\n")

