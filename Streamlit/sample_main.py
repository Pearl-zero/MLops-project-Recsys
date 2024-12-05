import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '9934b75338695cd7022c1f4c5ebea034'

#한국어 패치
#tmdb.language = 'ko-KR' 
#https://www.themoviedb.org/?language=ko

def get_recommendations(title):
    #     # Get the index of the movie that matches the title
    # if title not in indices:
    #     raise ValueError(f"Title '{title}' not found in indices.")
    
    idx = movies[movies['title']== title].index[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx].flatten()))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies (excluding the first which is itself)
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        
        try:
            print(f"Fetching details for movie title: {title}")
            print(f"Movie ID: {id}")  # Log the movie ID
            details = movie.details(id)
            # Process details as needed
        except TMDbException as e:
            print(f"Error fetching movie details: {e}")
            return None, None
        except Exception as e:  # Catch other exceptions
            print(f"An unexpected error occurred: {e}")
            return None, None
        
        # details = movie.details(id) 
        # https://developer.themoviedb.org/reference/movie-details
        
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'  
            
        images.append(image_path)
        titles.append(details['title'])                       
                        
    return images, titles        

    # Ensure indices are valid and within bounds
    # max_index = df_merged.shape[0] - 1
    # movie_indices = [i for i in movie_indices if i <= max_index]

    # # Return the top 10 most similar movies
    # return df_merged['title'].iloc[movie_indices]

movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb')) 
            
st.set_page_config(layout='wide')
st.header('6teamflix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)

if st.button('Recommend'):
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title) 

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(title[idx])
                idx += 1
