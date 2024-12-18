import React, { useEffect, useState } from "react";
import { fetchAllSongs, searchSongByTitle, downloadAllSongs, updateSongRatings } from "../Api";
import ReactPaginate from "react-paginate";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStar as filledStar } from "@fortawesome/free-solid-svg-icons";
import { faStar as emptyStar } from "@fortawesome/free-regular-svg-icons";
import "./Dashboard.css";

const Dashboard = () => {
  const [songs, setSongs] = useState([]);
  const [originalSongs, setOriginalSongs] = useState([]);
  const [page, setPage] = useState(1);
  const [searchMode, setSearchMode] = useState(false);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  useEffect(() => {
    if (!searchMode) {
      loadSongs(page);
    }
  }, [page, searchMode]);

  const loadSongs = async (pageNumber) => {
    const data = await fetchAllSongs(pageNumber, 10);
    setSongs(data);
    setOriginalSongs(data); 
  };

  const handleSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });

    const sortedSongs = [...songs].sort((a, b) => {
      if (a[key] < b[key]) return direction === "asc" ? -1 : 1;
      if (a[key] > b[key]) return direction === "asc" ? 1 : -1;
      return 0;
    });

    setSongs(sortedSongs);
  };

  const handleSearch = async (title) => {
    if (!title.trim()) {
      setSongs(originalSongs);
      setSearchMode(false);
      return;
    }

    try {
      const song = await searchSongByTitle(title);
      setSongs([song]);
      setSearchMode(true);
    } catch (error) {
      console.error("Song not found:", error);
      setSongs([]);
      setSearchMode(true);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await downloadAllSongs();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "songs.csv");
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error("Error downloading songs:", error);
    }
  };

  const handleStarClick = async (songId, rating) => {
    try {
      await updateSongRatings(songId, rating);
      const updatedSongs = songs.map((song) => {
        if (song.id === songId) song.rating = rating;
        return song;
      });
      setSongs(updatedSongs);
    } catch (error) {
      console.error("Error updating rating:", error);
    }
  };

  return (
    <div>
      <div className="search-container">
        <input
          type="text"
          placeholder="Search by song title"
          onChange={(e) => handleSearch(e.target.value)}
        />
        <button onClick={handleDownload}>Download All Songs</button>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th onClick={() => handleSort("id")}>ID</th>
            <th onClick={() => handleSort("title")}>Title</th>
            <th onClick={() => handleSort("danceability")}>Danceability</th>
            <th onClick={() => handleSort("energy")}>Energy</th>
            <th onClick={() => handleSort("key")}>Key</th>
            <th onClick={() => handleSort("loudness")}>Loudness</th>
            <th onClick={() => handleSort("mode")}>Mode</th>
            <th onClick={() => handleSort("acousticness")}>Acousticness</th>
            <th onClick={() => handleSort("instrumentalness")}>Instrumentalness</th>
            <th onClick={() => handleSort("liveness")}>Liveness</th>
            <th onClick={() => handleSort("valence")}>Valence</th>
            <th onClick={() => handleSort("tempo")}>Tempo</th>
            <th onClick={() => handleSort("duration_ms")}>Duration in MS</th>
            <th onClick={() => handleSort("time_signature")}>Time Signature</th>
            <th onClick={() => handleSort("num_bars")}>Number of Bars</th>
            <th onClick={() => handleSort("num_sections")}>Number of Sections</th>
            <th onClick={() => handleSort("num_segments")}>Number of Segments</th>
            <th onClick={() => handleSort("class")}>Class</th>
            <th onClick={() => handleSort("rating")}>Rating</th>
          </tr>
        </thead>
        <tbody>
          {songs.map((song, index) => (
            <tr key={index}>
              <td>{song.id}</td>
              <td>{song.title}</td>
              <td>{song.danceability}</td>
              <td>{song.energy}</td>
              <td>{song.key}</td>
              <td>{song.loudness}</td>
              <td>{song.mode}</td>
              <td>{song.acousticness}</td>
              <td>{song.instrumentalness}</td>
              <td>{song.liveness}</td>
              <td>{song.valence}</td>
              <td>{song.tempo}</td>
              <td>{song.duration_ms}</td>
              <td>{song.time_signature}</td>
              <td>{song.num_bars}</td>
              <td>{song.num_sections}</td>
              <td>{song.num_segments}</td>
              <td>{song.class}</td>
              <td>
                {[1, 2, 3, 4, 5].map((star) => (
                  <FontAwesomeIcon
                    key={star}
                    icon={star <= (song.rating || 0) ? filledStar : emptyStar}
                    onClick={() => handleStarClick(song.id, star)}
                    style={{ cursor: "pointer", color: star <= (song.rating || 0) ? "gold" : "gray" }}
                  />
                ))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {!searchMode && (
        <ReactPaginate
          previousLabel={"Previous"}
          nextLabel={"Next"}
          breakLabel={"..."}
          pageCount={10}
          marginPagesDisplayed={2}
          pageRangeDisplayed={3}
          onPageChange={(data) => setPage(data.selected + 1)}
          containerClassName={"pagination"}
          activeClassName={"active"}
        />
      )}
    </div>
  );
};

export default Dashboard;
