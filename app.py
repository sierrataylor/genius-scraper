import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/lyrics", methods=["GET", "POST"])
def run():
    artist = request.form["artist"]
    song = request.form["song"]

    title = "{} by {}".format( song.upper(), artist.upper())

    artist = artist.replace(" ", "-")
    artist += "-"
    song = song.lower()
    song = song.replace(" ", "-")
    song += "-lyrics"

    url = "https://genius.com/{0}{1}".format(artist, song)
    page = requests.get(url)

    #creating BeautifulSoup object
    soupSong = BeautifulSoup(page.text, "html.parser")

    try:
        lyrics = soupSong.find("div", class_="lyrics").get_text()
        print(lyrics)
    except AttributeError:
        print("Song not found, sorry!")
    return render_template("lyrics.html", lyrics=lyrics, title=title)

if __name__ == "__main__":
    app.run(debug=True)