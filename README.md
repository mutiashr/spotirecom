# 🎵 Spotify Song Recommendation System

This song recommendation system helps users discover new songs based on the songs they choose. By using processed Spotify song data, this app will provide song recommendations that are similar to the user's musical preferences.

## Features

- **Song and Artist Search**: Users can search for specific songs or artists available in the database.
- **Select Favorite Songs**: Users can choose 3-5 of their favorite songs from the available song list.
- **Song Recommendations**: Based on the user's selected songs, the system will provide 5 song recommendations that are similar.
- **Song Type Description**: The system provides a description of the song type chosen by the user based on musical features such as energy, danceability, and mood.

## Requirements

- Python 3.7 or higher
- Streamlit
- Pandas
- Pickle
- A CSV file containing processed Spotify song data (`processed_spotify_data.csv`)
- A pre-processed similarity matrix (`similarity_matrix.pkl`)

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone <your-repository-url>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure you have the `processed_spotify_data.csv` and `similarity_matrix.pkl` files in the same directory as this script. You can obtain these files from Google Colab or from other data processing steps.

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open the app in your browser using the link displayed in the terminal.

### Usage Flow:
1. **Song List**: The app displays a list of available songs in the database, including the song title, artist name, and album.
2. **Select Songs**: Users can choose 3-5 of their favorite songs. Each song is displayed with its artist name to make selection easier.
3. **Get Recommendations**: After selecting the songs, users can click a button to get song recommendations based on the similarity to the selected songs.
4. **Song Type Description**: The app also provides a description of the selected songs' type based on musical features like energy, danceability, and mood.

## Directory Structure

```
/project-root
├── app.py                       # Main Streamlit application script
├── processed_spotify_data.csv    # CSV file with processed Spotify song data
├── similarity_matrix.pkl        # Pre-processed song similarity matrix
└── requirements.txt             # List of Python dependencies
```

## Notes

- Make sure the `processed_spotify_data.csv` and `similarity_matrix.pkl` files are processed and ready for use.
- The recommendation system is based on a pre-calculated song similarity matrix, which depends on musical features like tempo, energy, and mood.

## Contributing

If you'd like to contribute to this project, please fork this repository and submit a pull request with any improvements or new features. We welcome contributions that can improve recommendation accuracy or add new features.
