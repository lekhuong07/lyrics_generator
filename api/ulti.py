import lyricsgenius
from secret_token import TOKEN

from search_api import get_artist, get_lyrics
from spacy.lang.en import English
import string
from tqdm.notebook import tqdm

nlp = English()
tokenizer = nlp.tokenizer


def get_average_song_length(artist_name, num_songs=5):
    artist = get_artist(artist_name, num_songs)
    result = []
    for s in artist.songs:
        lines = s.lyrics.split("\n")
        print(line)
        result.append("<s>")
        for line in lines:
            for w in tokenizer(line.strip().lower()):
                if w.text not in string.punctuation:
                    result.append(w.text)
        result.append("</s>")
        print("\n")
    return result


# Get a certain n-gram:
def get_ngrams(input_list, n):
    ngrams = {}
    for i in range(len(input_list) - (n - 1)):
        t = tuple(input_list[i:i + n])
        ngrams[t] = ngrams.get(t, 0) + 1
    return ngrams


# Get up to n-gram:
def get_upto_ngrams(input_list, n):
    ngrams = {}
    for i in range(1, n + 1):
        ngrams[i] = get_ngrams(input_list, i)
    return ngrams


# ngram is all the possible gram
# term is a tuple (A, B),
# len(term) == 1 -> unigram
# len(term) > 1-> has term needs to be calculated B, given term A (A is a tuple):
def calculate_prob(ngram, term):
    if len(term) == 1:
        a = sum([s for s in ngram[1].values()])
        b = ngram[1][term]
        result = ngram[1][term] / sum([s for s in ngram[1].values()])
        return result
    # else:
    else:
        A = term[:-1]  # n-1 gram
        if len(term) > len(ngram):
            return None
        return ngram[len(term)][term] / ngram[len(A)][A]


def list_to_sentence(input):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for s in input:
        str1 += s
        str1 += " "

        # return string
    return str1


if __name__ == "__main__":
    genius = lyricsgenius.Genius(TOKEN)
    artist = genius.search_artist("Kanye West", max_songs=3)
    lyrics = get_lyrics(artist)
