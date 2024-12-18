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

        update_data = request.json
        print('Hello:', update_data)
        for key, value in update_data.items():
            data.at[song_index[0], key] = value

        return jsonify({"message": "Song rating updated successfully", "updated_song": data.loc[song_index[0]].to_dict()})
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
