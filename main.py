import lyricsgenius
import os
from secret_token import TOKEN

if __name__ == "__main__":
    genius = lyricsgenius.Genius(TOKEN)
    artist = genius.search_artist("Lady Gaga", max_songs=10)
    #song = genius.search_songs("Dynamite", per_page=10, page=1)
    print(artist.songs)


