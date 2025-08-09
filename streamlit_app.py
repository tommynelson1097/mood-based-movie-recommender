import streamlit as st
from functions import fetch_movies_from_tmdb, generate_movie_recommendations

st.set_page_config(page_title="Mood-Based Movie Recommender", layout="centered")
st.title("🎬 Mood-Based Movie Recommender")
st.write("Select your mood and preferences to get personalized movie recommendations!")

# Mood options based on your mapping
mood_options = [
    'happy', 'sad', 'excited', 'romantic', 'scared', 'curious', 'fantasy', 'mysterious', 'inspired', 'sci-fi'
]

with st.form("movie_form"):
    mood = st.selectbox("How are you feeling?", mood_options, index=0)
    decade = st.selectbox("Choose a decade:", [1980, 1990, 2000, 2010, 2020], index=2)
    min_rating = st.slider("Minimum TMDB rating:", 0.0, 10.0, 7.0, 0.1)
    country = st.text_input("Country (2-letter code, e.g., US, GB, IN):", value="US")
    n = st.slider("How many recommendations?", 1, 10, 3)
    submitted = st.form_submit_button("Get Recommendations!")

if submitted:
    with st.spinner("Fetching movies and generating recommendations..."):
        try:
            movies = fetch_movies_from_tmdb(mood, decade, min_rating, country)
            if not movies:
                st.warning("No movies found for your criteria. Try adjusting your filters.")
            else:
                output = generate_movie_recommendations(mood, movies, n)
                st.markdown("---")
                st.subheader("Recommended Movies:")
                st.write(output)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by TMDB and OpenAI | Built with Streamlit")
