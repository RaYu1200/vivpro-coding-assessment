from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import os
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join("data", "songs.json")
columns = []

def normalize_data(json_file):
    """
    Normalize JSON data.
    """
    try:
        print("Normalizing data...")
        with open(DATA_FILE, 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                columns.append(item)
            result = pd.DataFrame(data, columns=columns)
            result["rating"] = None
        return result
    except Exception as e:
        print(f"Error normalizing/loading data: {e}")
        return pd.DataFrame()

data = normalize_data(DATA_FILE)
ratings_dir = {index: [] for index in range(len(data))}

@app.route("/songs", methods=["GET"])
def get_all_songs():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))
        start = (page - 1) * size
        end = start + size
        songs = data.iloc[start:end].to_dict(orient="records")
        return jsonify(songs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/songs/<title>", methods=["GET"])
def get_song_by_title(title):
    try:
        song = data[data["title"].str.lower() == title.lower()]
        if not song.empty:
            return jsonify(song.to_dict(orient="records")[0])
        else:
            return jsonify({"error": "Song not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/songs/<song_id>/rate", methods=["PUT"])
def rate_song(song_id):
    try:
        song_index = data[data["id"] == song_id].index
        if song_index.empty:
            return jsonify({"error": "Song not found"}), 404

        song_index = song_index[0]
        update_data = request.json
        if "rating" not in update_data:
            return jsonify({"error": "Missing 'rating' in request"}), 400

        new_rating = update_data.get("rating")
        if not isinstance(new_rating, (int, float)) or not (1 <= new_rating <= 5):
            return jsonify({"error": "Rating must be a number between 1 and 5"}), 400

        if song_index not in ratings_dir:
            ratings_dir[song_index] = []
        ratings_dir[song_index].append(int(new_rating))
        
        all_ratings = ratings_dir[song_index]
        avg_rating = sum(all_ratings) / len(all_ratings)
        data.at[song_index, "rating"] = avg_rating

        return jsonify({"message": "Song rating updated successfully", "updated_song": data.loc[song_index].to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/songs/download", methods=["GET"])
def download_songs():
    try:
        download_file = "songs.csv"
        data.to_csv(download_file, index=False)
        return send_file(download_file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
