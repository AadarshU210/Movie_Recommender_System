import streamlit as st
import pickle
import pandas as pd
import requests

API_Token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjOTZhOGZiZTk1YzYwMDJmNzk3MmI0MjU4OWUwY2U4ZSIsIm5iZiI6MTc2MzEzNDAzOS4xNzIsInN1YiI6IjY5MTc0YTU3NmNiM2U1Yjg1NzRjOWIxOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.cWwIXuxC26eekBwNcD80v2ZMcp_7SjchQkv6-RVYNJc"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    
    headers = {
        "Authorization": f"Bearer {API_Token}",
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        posters = data.get("posters")
        if posters and len(posters) > 0:
            poster_path = posters[0].get("file_path")
            return "https://image.tmdb.org/t/p/original" + poster_path
        
        return "https://via.placeholder.com/500x750?text=No+Image"

    except Exception as e:
        print("API ERROR:", e)
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Select movie or Enter movie name", movies['title'].values
)
    
if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])

