import pickle
import streamlit as st
import pandas as pd
import gdown
import os

# Download pkl files from Google Drive if not present
if not os.path.exists('movies.pkl'):
    gdown.download('https://drive.google.com/uc?id=1Xo2bB9b54ytI-0LDkl_7SSj1lfvK8prC',
                   'movies.pkl', quiet=False)

if not os.path.exists('movies_dict.pkl'):
    gdown.download('https://drive.google.com/uc?id=14kRYDG2b1-1LrAbinKe5HY9NOVALIEpi',
                   'movies_dict.pkl', quiet=False)

if not os.path.exists('similarity.pkl'):
    gdown.download('https://drive.google.com/uc?id=1rlMfhCWdECTJ-pS8_akjEWTydl__vaRM',
                   'similarity.pkl', quiet=False)


# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader('Top 5 Similar Movies:')
    for i, movie in enumerate(recommendations, 1):
        st.write(f"{i}. {movie}")