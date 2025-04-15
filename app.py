import streamlit as st
import pickle
import requests
import time
import random


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=75b1b624eaac7c3d264e5bda052a0b09&language=en-US"

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)

    return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


def surprise_me():
    random_movies = movies.sample(10)
    random_movie_names = random_movies['title'].tolist()
    random_movie_posters = [fetch_poster(mid) for mid in random_movies['movie_id'].tolist()]
    return random_movie_names, random_movie_posters


# Streamlit UI
# Streamlit UI
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Type or select a movie from the dropdown", movie_list)

# Buttons in one row
# Buttons in a row (side by side)
spacer1, col1, col2, spacer2 = st.columns([1, 2, 2, 1])

with col1:
    recommend_clicked = st.button('🎥 Show Recommendation')

with col2:
    surprise_clicked = st.button('🎲 Surprise Movies!')


# Show recommendations
if recommend_clicked:
    st.markdown("<h2 style='text-align: center;'>✨ Top Movies Based on Your Recommendation</h2>", unsafe_allow_html=True)
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols1 = st.columns(5, gap="large")
    for i in range(5):
        with cols1[i]:
            st.markdown(f"<h4 style='text-align: center;'>{recommended_movie_names[i]}</h4>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i], use_container_width=True)

    cols2 = st.columns(5, gap="large")
    for i in range(5, 10):
        with cols2[i - 5]:
            st.markdown(f"<h4 style='text-align: center;'>{recommended_movie_names[i]}</h4>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i], use_container_width=True)

# Show random surprise movies
if surprise_clicked:
    st.markdown("<h2 style='text-align: center;'>🎁 Surprise Movies Just for You!</h2>", unsafe_allow_html=True)
    random_movie_names, random_movie_posters = surprise_me()

    cols1 = st.columns(5, gap="large")
    for i in range(5):
        with cols1[i]:
            st.markdown(f"<h4 style='text-align: center;'>{random_movie_names[i]}</h4>", unsafe_allow_html=True)
            st.image(random_movie_posters[i], use_container_width=True)

    cols2 = st.columns(5, gap="large")
    for i in range(5, 10):
        with cols2[i - 5]:
            st.markdown(f"<h4 style='text-align: center;'>{random_movie_names[i]}</h4>", unsafe_allow_html=True)
            st.image(random_movie_posters[i], use_container_width=True)

