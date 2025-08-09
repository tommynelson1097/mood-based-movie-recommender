# Mood-Based Movie Recommender

This project is a web application that recommends movies based on your current mood, using The Movie Database (TMDB) API and OpenAI's GPT model. The app is built with Streamlit for an interactive user experience.

## Features
- Select your mood, preferred decade, minimum TMDB rating, and country of origin
- Fetches relevant movies from TMDB
- Uses OpenAI GPT to generate friendly, mood-matched movie recommendations with descriptions
- Secure API key management using a `.env` file

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd mood-based-movie-recommender
```

### 2. Install Dependencies
Install required Python packages:
```
pip install streamlit openai requests python-dotenv
```

### 3. Set Up API Keys
Create a `.env` file in the project root with the following content:
```
TMDB_API_KEY=your_tmdb_api_key
OPENAI_API_KEY=your_openai_api_key
```
Replace `your_tmdb_api_key` and `your_openai_api_key` with your actual API keys.

### 4. Run the App
Start the Streamlit app:
```
streamlit run streamlit_app.py
```

## File Structure
- `streamlit_app.py` - Main Streamlit web app
- `functions.py` - Core logic for fetching movies and generating recommendations
- `.env` - Environment variables for API keys (not included in version control)

## Notes
- You need valid TMDB and OpenAI API keys to use this app.
- The app uses GPT to select and describe movies from the TMDB results, but recommendations may not always perfectly match the mood.
- For best results, try different moods and filters.

## License
This project is for educational and personal use. See `LICENSE` for more details.
