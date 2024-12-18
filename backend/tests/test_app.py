import pytest
from app import app, data

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_all_songs(client):
    response = client.get("/songs?page=1&size=10")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) <= 10

def test_get_all_songs_invalid_page(client):
    response = client.get("/songs?page=abc&size=10")
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data

def test_get_song_by_title(client):
    song_title = data.iloc[0]["title"]
    response = client.get(f"/songs/{song_title}")
    assert response.status_code == 200
    song = response.get_json()
    assert song["title"].lower() == song_title.lower()

def test_get_song_by_title_not_found(client):
    response = client.get("/songs/nonexistenttitle")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Song not found"

def test_rate_song(client):
    song_id = data.iloc[0]["id"]
    payload = {"rating": 4}
    response = client.put(f"/songs/{song_id}/rate", json=payload)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["message"] == "Song rating updated successfully"
    assert response_data["updated_song"]["rating"] == 4

def test_rate_song_invalid_id(client):
    response = client.put("/songs/invalid-id/rate", json={"rating": 4})
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Song not found"

def test_download_songs(client):
    response = client.get("/songs/download")
    assert response.status_code == 200
    assert response.content_type.startswith("text/csv")
    assert "attachment" in response.headers["Content-Disposition"]