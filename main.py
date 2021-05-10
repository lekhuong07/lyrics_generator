import lyricsgenius
import os
from secret_token import TOKEN
from flask import Flask, request, jsonify
import api.ngram as ngram
import api.search_api as apisa
import api.analysis as apia

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/SEARCH_ARTISTS', methods=['GET'])
def search_artists():
    search_term = request.args.get('search_term') or ""
    per_page = request.args.get('per_page') or 10
    page_number = request.args.get('page_number') or 1
    genius = lyricsgenius.Genius(TOKEN)
    artists = genius.search_artists(search_term, per_page, page_number)
    return artists


@app.route('/GET_ALL_ARTISTS', methods=['GET'])
def get_artists():
    per_page = request.args.get('per_page') or 10
    page_number = request.args.get('page_number') or 1
    genius = lyricsgenius.Genius(TOKEN)
    artists = genius.search_artists("*", per_page, page_number)
    return artists


if __name__ == "__main__":
    #app.run(threaded=True, port=5000)

    #lyrics = []
    #for song in artist.songs:
    #    tokens = song.lyrics.split(" ")
        #lyrics.extend(tokens)
    genius = lyricsgenius.Genius(TOKEN)
    artist = genius.search_artist("Lady Gaga", max_songs=10)
    lyrics = apisa.get_lyrics(artist)
    print("Generate with NGramLM")
    model = ngram.NGramLM(lyrics, 3)
    result = model.generate_song(artist)
    print(result)
