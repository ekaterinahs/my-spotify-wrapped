# 🎶 Spotify Playlist Analysis Dashboard

This repository contains the code for the **"Spotify Playlist Analysis"** web application, built using Streamlit. The tool allows users to input a Spotify playlist link and performs various analyses on the playlist. The analysis includes the most frequent artists, average song popularity, and individual song characteristics like release date and popularity, providing a deep dive into the playlist's composition.

***

## 📊 Data
To run the analysis, the application pulls data directly from the Spotify API using the playlist URL provided by the user. Key data points extracted include song metadata such as: song name, artist(s), popularity score, release date, album name... This information is then analyzed and visualized to give insights into the playlist's characteristics.

### 📁 Files
- app.py - the main Streamlit app file, which runs the web interface.
- requirements.txt - list of dependencies required to run the project, including libraries like Streamlit, Spotipy, and Pandas.
- my_pages/ - folder containing various scripts used for different analysis and visualizations.

***

To use the application, **you must obtain your own Spotify API credentials**, which can be done by registering your application on Spotify Developer Dashboard.

## 🔎 Features
Once you enter the Spotify playlist link, the application performs the following analyses:

- ***Top Artists by Number of Songs:*** Identifies the most frequent artists within the playlist based on song count.
- ***Mean Song Popularity:*** Computes the average popularity score for all songs within the playlist.
- ***Individual Song Popularity:*** Displays the popularity score for each song in the playlist.
- ***Release Dates:*** Shows the release dates of the songs in the playlist, allowing you to see how recent the tracks are.

The tool then generates a series of visualizations and summary statistics for each of these features.

***

## 🚀 Getting Started
To get the application up and running locally, follow these steps:

1. Clone the repository:

`git clone https://github.com/ekaterinahs/spotify-playlist-analyzer.git`
`cd spotify-playlist-analyzer`

2. Install dependencies:

`pip install -r requirements.txt`

3. Run the Streamlit app:

`streamlit run streamlit_app.py`

4. Open the application in your browser at http://localhost:8501.
