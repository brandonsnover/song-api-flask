from flask import Flask, request, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/songs.json")
def index():
    return db.songs_all()

@app.route("/songs.json", methods=["POST"])
def create():
    title = request.form.get("title")
    artist = request.form.get("artist")
    album = request.form.get("album")
    duration = request.form.get("duration")
    return db.songs_create(title, artist, album, duration)

@app.route("/songs/<id>.json")
def show(id):
    return db.songs_find_by_id(id)

@app.route("/songs/<id>.json", methods=["PATCH"])
def update(id):
    existing_data = db.songs_find_by_id(id)
    title = request.form.get("title", existing_data["title"])
    artist = request.form.get("artist", existing_data["artist"])
    album = request.form.get("album", existing_data["album"])
    duration = request.form.get("duration", existing_data["duration"])
    updated_data = db.songs_update_by_id(id, title, artist, album, duration)
    return jsonify(updated_data)

@app.route("/songs/<id>.json", methods=["DELETE"])
def destroy(id):
    return db.songs_destroy_by_id(id)