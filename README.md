# RedditUserPersona
A Python script that analyzes Reddit users' posts and comments to generate detailed personality profiles using Google's Gemini AI.

Features
- Input: Reddit user profile URL
- Fetches user data from Reddit (posts & comments)
- Uses Google's Gemini AI to generate AI-powered personality analysis
- Rate-limiting compliant (avoids API bans)
- Outputs a structured User Persona in .txt format
- Cites which post or comment supports each trait
- Comprehensive error logging

Tech used
Python 3
PRAW (Reddit API Wrapper)
Google Generative AI (Gemini Pro)
dotenv (.env file for API keys)

Steps to follow:
1. Install the following dependencies:
pip install praw python-dotenv google-generativeai

2. Create a .env file consisting of the following:
REDDIT_CLIENT_ID="your_reddit_app_id"
REDDIT_CLIENT_SECRET="your_reddit_app_secret"
REDDIT_USER_AGENT="app_name/version_number (by /u/your_reddit_username)"
GEMINI_API_KEY="your_google_api_key"

3. Run the script and enter a Reddit profile URL:
python persona_generator.py
example input: https://www.reddit.com/user/kojied/

Outputs will be saved in the outputs/ folder:
username_raw.txt: Raw posts/comments
username_persona.txt: AI-generated analysis

API Requirements
1. Reddit API:
Create an app at Reddit Preferences > Apps
Select "script" type
Note your client ID and secret

2. Google Gemini API:
Get an API key from Google AI Studio
