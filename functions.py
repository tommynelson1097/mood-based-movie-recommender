"""
Core logic for Mood-Based Movie Recommender (TMDB + OpenAI)
"""


import requests
import openai
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file at import time
load_dotenv()

# Example: Load API keys from Streamlit secrets if available, else from environment variables
def get_openai_key():
    try:
        import streamlit as st
        return st.secrets["OPENAI_API_KEY"]
    except (ImportError, KeyError, AttributeError):
        return os.getenv("OPENAI_API_KEY")

def get_tmdb_key():
    try:
        import streamlit as st
        return st.secrets["TMDB_API_KEY"]
    except (ImportError, KeyError, AttributeError):
        return os.getenv("TMDB_API_KEY")

# Map moods to TMDB genre IDs
mood_to_genre = {
    'happy': ['35', '10751'],        # Comedy, Family
    'sad': ['18'],                  # Drama
    'excited': ['28', '12'],        # Action, Adventure
    'romantic': ['10749'],          # Romance
    'scared': ['27', '53'],         # Horror, Thriller
    'curious': ['99'],              # Documentary
    'fantasy': ['14', '16'],        # Fantasy, Animation
    'mysterious': ['9648'],         # Mystery
    'inspired': ['36', '10402'],    # History, Music
    'sci-fi': ['878'],              # Science Fiction
}

def get_genres_for_mood(mood):
    """Return a list of genre IDs for a given mood."""
    return mood_to_genre.get(mood.lower(), ['18'])  # Default to Drama if not found

def fetch_movies_from_tmdb(mood, decade, min_rating, country):
    """Fetch movies from TMDB based on mood, decade, minimum rating, and country of origin. Requires TMDB_API_KEY in .env."""
    genres = get_genres_for_mood(mood)
    genre_str = ','.join(genres)
    start_date = f'{decade}-01-01'
    end_date = f'{decade+9}-12-31'
    # Use Streamlit secrets if available, else fallback to environment variable
    api_key = get_tmdb_key()
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": api_key,
        "with_genres": genre_str,
        "sort_by": "popularity.desc",
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "vote_average.gte": min_rating,
        "region": country.upper(),
    }
    response = requests.get(url, params=params)

    # Debug: print API key and full response for troubleshooting
    print("TMDB API Key:", api_key)
    print("TMDB URL:", response.url)
    print("TMDB Response:", response.json())
    
    return response.json().get("results", [])

def generate_movie_recommendations(mood, movies, n=3):
    """Use OpenAI GPT to recommend and describe n movies for the given mood, showing TMDB rating next to each film name. Requires OPENAI_API_KEY in .env."""
    openai_api_key = get_openai_key()
    if not openai_api_key:
        raise ValueError('OpenAI API key not found. Please add OPENAI_API_KEY to your .env file or Streamlit secrets.')
    openai.api_key = openai_api_key
    movie_list = '\n'.join([
        f"- {m['title']} (TMDB rating: {m.get('vote_average', 'N/A')}): {m.get('overview', 'No description available.')}" 
        for m in movies[:10]
    ])
    prompt = (
        f"User mood: {mood}\n"
        f"Here are some movies fetched from TMDB that might fit this mood (with their TMDB ratings):\n{movie_list}\n\n"
        f"Please recommend and describe {n} movies from this list that best fit the user's mood. For each recommended movie, you must display the TMDB rating next to the movie title in your output. Respond in a friendly, engaging way."
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content
