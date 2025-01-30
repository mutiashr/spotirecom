import streamlit as st
import pandas as pd
import pickle

# Load data processed from Google Colab
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_spotify_data.csv')  # Load your preprocessed data
        with open('similarity_matrix.pkl', 'rb') as f:  # Load the similarity matrix
            similarity_matrix = pickle.load(f)
        return df, similarity_matrix
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

df, similarity_matrix = load_data()

if df is None or similarity_matrix is None:
    st.stop()  # Stop execution if data loading fails

# Recommendation function with genre filter
def recommend_songs_with_genre(selected_songs, df, similarity_matrix, top_n=5):
    selected_genres = df[df['track_name'].isin(selected_songs)]['playlist_genre'].unique()
    
    selected_indices = df[df['track_name'].isin(selected_songs)].index
    avg_similarity = similarity_matrix[selected_indices].mean(axis=0)
    similar_songs_indices = avg_similarity.argsort()[::-1]

    recommended_songs = []
    for idx in similar_songs_indices:
        if idx not in selected_indices:
            # Filter songs by the same genre
            if df.iloc[idx]['playlist_genre'] in selected_genres:
                recommended_songs.append(df.iloc[idx])
            if len(recommended_songs) == top_n:
                break

    return pd.DataFrame(recommended_songs)

# Function to describe the song type
def describe_song_type(df, selected_songs):
    # Select only numeric columns
    numeric_features = df.select_dtypes(include=['float64', 'int64'])
    
    # Filter the dataframe by selected songs using track_name from the original df
    selected_df = df[df['track_name'].isin(selected_songs)]
    
    # Calculate the average feature values of the selected songs
    avg_features = selected_df[numeric_features.columns].mean()

    # Determine song type based on features
    energy_type = "energetic and full of energy" if avg_features['energy'] > 0.7 else "calm and relaxed"
    danceability_type = "easy to dance to" if avg_features['danceability'] > 0.7 else "better for relaxing"
    mood_type = "positive and cheerful" if avg_features['valence'] > 0.5 else "sad and melancholic"
    
    description = f"hmmzz... keknya tipe lagu kamu ini yang {energy_type}, {danceability_type}, and {mood_type} gitu yaaah.... enih rekomendasinya:"
    return description

# Streamlit UI
st.title('🎵 Sistem Rekomendasi Lagu Spotify✨')
st.markdown("<small>Credit: enih project punya mutiw @sahiroww </small>", unsafe_allow_html=True)

st.write("### Song List")
st.dataframe(df[['track_name', 'track_artist', 'track_album_name']])

st.write("### Choose 3-5 Favorite Songs")

# Display options with song name and artist name
unique_songs = df.drop_duplicates(subset=['track_name', 'track_artist'])
selected_songs = st.multiselect(
    "Pick songs:",
    unique_songs['track_name'].unique(),
    format_func=lambda x: f"{x} - {unique_songs[unique_songs['track_name'] == x]['track_artist'].values[0]}",
    max_selections=5
)

if st.button("Get Recommendations"):
    if len(selected_songs) >= 3:
        # Get the description of the selected songs
        description = describe_song_type(df, selected_songs)
        st.write(description)

        # Get song recommendations based on the selected songs
        recommendations = recommend_songs_with_genre(selected_songs, df, similarity_matrix)
        st.write("### Recommended Songs 🎶")
        st.dataframe(recommendations[['track_name', 'track_artist', 'track_album_name']])
    else:
        st.error("Please select at least 3 songs.")
