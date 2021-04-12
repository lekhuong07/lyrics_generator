import lyricsgenius
import os
from secret_token import TOKEN
from flask import Flask, request, jsonify
from commands import app

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
    #genius = lyricsgenius.Genius(TOKEN)
    #artist = genius.search_artist("Lady Gaga", max_songs=10)
    #song = genius.search_songs("Dynamite", per_page=10, page=1)
    #print(artist.songs)


