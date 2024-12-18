import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_all_songs(client):
    response = client.get("/songs?page=1&size=10")
    assert response.status_code == 200

def test_get_song_by_title(client):
    response = client.get("/songs/3AM")
    assert response.status_code == 200

def test_rate_song(client):
    response = client.post("/songs/1/rate", json={"rating": 5})
    assert response.status_code == 200
