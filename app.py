import streamlit as st
import pandas as pd
import pickle

# Load data processed dari Google Colab
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_spotify_data.csv')
        with open('similarity_matrix.pkl', 'rb') as f:
            similarity_matrix = pickle.load(f)
        return df, similarity_matrix
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

df, similarity_matrix = load_data()

if df is None or similarity_matrix is None:
    st.stop()  # Jika data gagal dimuat, hentikan eksekusi lebih lanjut

# Fungsi rekomendasi
def recommend_songs(selected_songs, df, similarity_matrix, top_n=5):
    selected_indices = df[df['track_name'].isin(selected_songs)].index
    avg_similarity = similarity_matrix[selected_indices].mean(axis=0)
    similar_songs_indices = avg_similarity.argsort()[::-1]

    recommended_songs = []
    for idx in similar_songs_indices:
        if idx not in selected_indices:
            recommended_songs.append(df.iloc[idx])
            if len(recommended_songs) == top_n:
                break

    return pd.DataFrame(recommended_songs)

# Fungsi untuk mendeskripsikan tipe lagu
def describe_song_type(df, selected_songs):
    # Pilih hanya kolom numerik
    numeric_features = df.select_dtypes(include=['float64', 'int64'])
    
    # Filter berdasarkan lagu yang dipilih menggunakan track_name dari df asli
    selected_df = df[df['track_name'].isin(selected_songs)]
    
    # Ambil rata-rata fitur dari lagu yang dipilih
    avg_features = selected_df[numeric_features.columns].mean()

    # Tentukan tipe lagu berdasarkan beberapa fitur
    energy_type = "enerjik dan penuh semangat" if avg_features['energy'] > 0.7 else "tenang dan santai"
    danceability_type = "mudah untuk berdansa" if avg_features['danceability'] > 0.7 else "lebih cocok untuk mendengarkan secara santai"
    mood_type = "positif dan ceria" if avg_features['valence'] > 0.5 else "sedih dan melankolis"
    
    description = f"Sepertinya kamu menyukai lagu yang {energy_type}, {danceability_type}, dan {mood_type}. Berikut rekomendasi lagu untukmu:"
    return description

# Tampilan Streamlit
st.title('🎵 Sistem Rekomendasi Lagu Spotify')

st.write("### Daftar Lagu")
st.dataframe(df[['track_name', 'track_artist', 'track_album_name']])

st.write("### Pilih 3-5 Lagu Favorit Anda")

# Menampilkan pilihan dengan format nama lagu + nama artis
unique_songs = df.drop_duplicates(subset=['track_name', 'track_artist'])
selected_songs = st.multiselect(
    "Pilih lagu:",
    unique_songs['track_name'].unique(),
    format_func=lambda x: f"{x} - {unique_songs[unique_songs['track_name'] == x]['track_artist'].values[0]}",
    max_selections=5
)

if st.button("Dapatkan Rekomendasi"):
    if len(selected_songs) >= 3:
        # Mendapatkan deskripsi tipe lagu yang dipilih
        description = describe_song_type(df, selected_songs)
        st.write(description)

        # Mendapatkan rekomendasi lagu
        recommendations = recommend_songs(selected_songs, df, similarity_matrix)
        st.write("### Rekomendasi Lagu 🎶")
        st.dataframe(recommendations[['track_name', 'track_artist', 'track_album_name']])
    else:
        st.error("Silakan pilih minimal 3 lagu.")
