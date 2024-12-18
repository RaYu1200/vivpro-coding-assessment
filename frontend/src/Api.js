import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

export const fetchAllSongs = async (page = 1, size = 10) => {
  const response = await axios.get(`${API_BASE_URL}/songs?page=${page}&size=${size}`);
  return response.data;
};

export const searchSongByTitle = async (title) => {
  const response = await axios.get(`${API_BASE_URL}/songs/${title}`);
  return response.data;
};

export const updateSongRatings = async (song_id, rating) => {
    const response = await axios.put(`${API_BASE_URL}/songs/${song_id}/rate`, { rating });
    return response.data;
};
  
export const downloadAllSongs = async () => {
  const response = await axios.get(`${API_BASE_URL}/songs/download`, { responseType: "blob" });
  return response;
};
