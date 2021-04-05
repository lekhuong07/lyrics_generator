import lyricsgenius
import os, sys
from secret_token import TOKEN


def get_artist(artist_name):
    genius = lyricsgenius.Genius(TOKEN)
    artist = genius.search_artist(artist_name, max_songs=0)
    return artist

def get_lyrics(song_name):
    genius = lyricsgenius.Genius(TOKEN)
    song = genius.search_lyrics(song_name)
    return song

def get_artist_songs(num_songs, ):
    genius = lyricsgenius.Genius(TOKEN)
    artist = get_artist("Lady Gaga")


if __name__ == "__main__":
    genius = lyricsgenius.Genius(TOKEN)
    artist = get_artist("Lady Gaga")
    print("Artist id:", artist._body['api_path'])
    art = genius.artist_songs(447)
    print(len(art['songs']))
    for s in art['songs']:
        print(s.keys())
        break

