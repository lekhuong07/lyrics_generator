from flask import Flask, request, jsonify
import lyricsgenius

app = Flask(__name__)
app.config["DEBUG"] = True
TOKEN = "_og96oiUYFvX26kqqK9I5bi4lrbCdgFp8SiHGxmjKxV7HWozBIXxEDF9GHA7gXaU"  # These access tokens never expire


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
