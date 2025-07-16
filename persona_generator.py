import os
import time
import re
import logging
import praw
import google.generativeai as genai
from dotenv import load_dotenv


logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filename = 'persona_generator.log'
)


load_dotenv()


try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key = GEMINI_API_KEY)
    
    reddit = praw.Reddit(
        client_id = os.getenv("REDDIT_CLIENT_ID"),
        client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent = os.getenv("REDDIT_USER_AGENT", "PersonaGenerator/1.0 (by /u/YourUsername)")
    )
except Exception as e:
    logging.error(f"API initialization failed: {e}")
    raise

def fetch_user_data(username):
    redditor = reddit.redditor(username)
    posts, comments = [], []
    
    try:
        for submission in redditor.submissions.new(limit = 10):
            if submission.selftext:
                posts.append(f"Title: {submission.title}\nBody: {submission.selftext}\n")
            time.sleep(2)
            
        for comment in redditor.comments.new(limit = 20):
            comments.append(f"Comment: {comment.body}\n")
            time.sleep(1)
            
    except Exception as e:
        logging.error(f"Error fetching data for {username}: {e}")
        raise
        
    return posts, comments

def save_to_file(username, posts, comments):
    try:
        os.makedirs("outputs", exist_ok = True)
        output_path = f"outputs/{username}_raw.txt"
        
        with open(output_path, "w", encoding = "utf-8") as f:
            if posts:
                f.write("--- POSTS ---\n\n")
                f.write("\n".join(posts))
            if comments:
                f.write("\n\n--- COMMENTS ---\n\n")
                f.write("\n".join(comments))
                
        logging.info(f"Data saved to {output_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
        return False

def generate_persona_from_text(text):
    try:
        model = genai.GenerativeModel(model_name = "models/gemini-1.5-flash")
        
        prompt = f"""Analyze this Reddit user's activity and create a detailed persona:
        
        Required Format:
        - Name: [Creative nickname based on username]
        - Age Range: [Estimated]
        - Occupation: [Inferred from content]
        - Personality: [3-5 traits]
        - Key Interests: [Top 3 topics]
        - Pain Points / Frustrations: [Any complaints or negative patterns?]
        - Frequent Subreddits: [List]
        - Behavioral Patterns: [Notable habits]
        - Quote: [Most representative comment]
        - Citations: [For each trait, mention the comment/post that supports it]
        
        User Activity:
        {text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return None

def generate_and_save_persona(username):
    raw_file = f"outputs/{username}_raw.txt"
    output_file = f"outputs/{username}_persona.txt"
    
    try:
        if not os.path.exists(raw_file):
            logging.error("Raw data not found")
            return False
            
        with open(raw_file, "r", encoding = "utf-8") as f:
            user_text = f.read()
            
        persona = generate_persona_from_text(user_text)
        if not persona:
            return False
            
        with open(output_file, "w", encoding = "utf-8") as f:
            f.write(persona)
            
        logging.info(f"Persona saved to {output_file}")
        return True
    except Exception as e:
        logging.error(f"Persona generation failed: {e}")
        return False

if __name__ == "__main__":
    try:
        print("Reddit Persona Generator")
        print("-----------------------")
        url = input("Enter Reddit profile URL: ").strip()
        
        if "/user/" not in url:
            print("Error: URL must contain '/user/'")
            exit()
            
        username = url.split("/user/")[1].split("/")[0]
        if not username:
            print("Error: Invalid username extracted")
            exit()
            
        print(f"\nFetching data for user: {username}...")
        posts, comments = fetch_user_data(username)
        
        if not posts and not comments:
            print("No data found for this user")
            exit()
            
        if save_to_file(username, posts, comments):
            print("\nGenerating persona...")
            if generate_and_save_persona(username):
                print("\nSuccess! Check the 'outputs' folder for results.")
            else:
                print("Persona generation failed")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
        logging.exception("Script crashed")
