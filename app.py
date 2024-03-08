import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=89aa350b846d47b961d05eb459bcf5c8&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data.get('poster_path')  # Use .get() method to handle None value
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None
        #print(data)
    #return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(movies.iloc[i[0]].title)

    recommend_movies = []
    recommended_movies_posters = []

    for i in distances[1:6]:
        movie_id= movies.iloc[i[0]].movie_id


        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)



if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)



    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])