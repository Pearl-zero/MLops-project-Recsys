import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '9934b75338695cd7022c1f4c5ebea034'
#https://www.themoviedb.org/?language=ko

movies = pickle.load(open('movies.pickle', 'rb'))
#cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))
            
st.set_page_config(layout='wide')
st.header('6teamflix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)

if st.button('Recommend'):
    pass 

