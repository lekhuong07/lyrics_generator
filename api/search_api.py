import lyricsgenius
import os, sys
from secret_token import TOKEN

from spacy.lang.en import English
import string
from tqdm.notebook import tqdm

nlp = English()
tokenizer = nlp.tokenizer


def get_artist(artist_name, num_songs):
    if num_songs > 50:
        return None
    api = lyricsgenius.Genius(TOKEN)
    artist = api.search_artist(artist_name, max_songs=num_songs)
    return artist


#artist = sa.get_artist(artist_name, num_songs)
#artist here is an object returned from the api call
def get_lyrics(artist):
    result = []
    analysis = {}

    for s in artist.songs:
        lines = s.lyrics.split("\n")
        result.append("<s>")
        for line in lines:
            if line != "":
                if line[0] != "[":
                    for w in tokenizer(line.rstrip().lower()):
                        word_text = w.text
                        # take care of can't, don't
                        if "'" in word_text:
                            word_text = word_text.replace("'", "")
                            result[len(result)-1] = result[len(result)-1] + word_text
                        else:
                            if word_text not in string.punctuation:
                                result.append(word_text)
        result.append("</s>")
    return result


if __name__ == "__main__":
    result = get_lyrics("Lady Gaga", 1)
    print(result)

    '''
    genius = lyricsgenius.Genius(TOKEN)
    art = genius.artist_songs(447)
    print(len(art['songs']))
    
    '''


