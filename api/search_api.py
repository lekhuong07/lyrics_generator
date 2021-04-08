import lyricsgenius
import os, sys
from secret_token import TOKEN


def get_artist(artist_name, num_songs):
    if num_songs > 50:
        return None
    api = lyricsgenius.Genius(TOKEN)
    artist = api.search_artist(artist_name,max_songs=num_songs)
    return artist


def get_lyrics(artist_name, num_songs):
    artist = get_artist(artist_name, num_songs)
    result = []
    for s in artist.songs:
        lines = s.lyrics.split("\n")
        result.append("<s>")
        for line in lines:
            if len(line.split(" ")) > 2:
                for w in line.split(" "):
                    result.append(w)
        result.append("</s>")
    return result


if __name__ == "__main__":
    result = get_lyrics("Lady Gaga", 3)
    print(result)

    '''
    genius = lyricsgenius.Genius(TOKEN)
    art = genius.artist_songs(447)
    print(len(art['songs']))
    
    '''


