import lyricsgenius
import os
from secret_token import TOKEN
from flask import Flask, request, jsonify

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
    app.run(threaded=True, port=5000)
    #genius = lyricsgenius.Genius(TOKEN)
    #artist = genius.search_artist("Lady Gaga", max_songs=10)
    #song = genius.search_songs("Dynamite", per_page=10, page=1)
    #print(artist.songs)


