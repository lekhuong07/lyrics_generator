import random
import math as ma
import lyricsgenius
from secret_token import TOKEN

from spacy.lang.en import English
import string
from tqdm.notebook import tqdm

nlp = English()
tokenizer = nlp.tokenizer


#artist = sa.get_artist(artist_name, num_songs)
#artist here is an object returned from the api call
def artist_analysis(artist):
    result = []
    analysis = {}
    num_songs = len(artist.songs)
    for s in artist.songs:
        lines = s.lyrics.split("\n")
        for line in lines:
            if line != "":
                if line[0] == "[":
                    if "Intro" in line:
                        if "Intro" not in analysis:
                            analysis["Intro"] = [0, 0]
                        analysis["Intro"][0] += 1
                        temp = "Intro"
                    elif "Verse" in line:
                        if "Verse" not in analysis:
                            analysis["Verse"] = [0, 0]
                        analysis["Verse"][0] += 1
                        temp = "Verse"
                    elif "Chorus" in line:
                        if "Chorus" not in analysis:
                            analysis["Chorus"] = [0, 0]
                        analysis["Chorus"][0] += 1
                        temp = "Chorus"
                    elif "Outro" in line:
                        if "Outro" not in analysis:
                            analysis["Outro"] = [0, 0]
                        analysis["Chorus"][0] += 1
                        temp = "Outro"
                else:
                    part_length = 0
                    for w in tokenizer(line.rstrip().lower()):
                        word_text = w.text
                        # take care of can't, don't
                        if "'" in word_text:
                            word_text = word_text.replace("'", "")
                            result[len(result)-1] = result[len(result)-1] + word_text
                            part_length += 1
                        else:
                            if word_text not in string.punctuation:
                                result.append(word_text)
                                part_length += 1
                    analysis[temp][1] += part_length

    print(analysis)
    for k in analysis.keys():
        if k == "Chorus":
            analysis[k][0] /= (num_songs*3)
            analysis[k][1] /= (num_songs*3)
        else:
            analysis[k][0] /= num_songs
            analysis[k][1] /= num_songs
    return analysis


if __name__ == "__main__":
    genius = lyricsgenius.Genius(TOKEN)
    artist = genius.search_artist("Lady Gaga", max_songs=50)
    result = artist_analysis(artist)
    print(result)