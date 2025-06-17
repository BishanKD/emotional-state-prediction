import os
import praw
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

subreddits = {
    "gratitude": 1.0,
    "happy": 0.9,
    "TodayIAmHappy": 0.8,
    "BenignExistence": 0.7,
    "Emotions": 0.6,
    "offmychest": 0.4,
    "vent": 0.3,
    "lonely": 0.2,
    "Anxiety": 0.1,
    "SuicideWatch": 0.0
}

def fetch_from_subreddit(subreddit, score, limit=500):
    print(f"Fetching from r/{subreddit}...")
    posts = []

    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        if submission.stickied or submission.score <= 1:
            continue

        title = submission.title
        selftext = submission.selftext or ''
        content = (title + "\n" + selftext).strip()

        if not title or not selftext:
            continue
        if len(content) < 30:  # Skip very short posts
            continue

        posts.append({
            'title': title,
            'selftext': selftext,
            'subreddit': subreddit,
            'created_utc': datetime.fromtimestamp(submission.created_utc),
            'id': submission.id,
            'emotional_score': score
        })
    print(f"Collected {len(posts)} posts from r/{subreddit}")
    return posts

all_data = []
for sub, score in subreddits.items():
    try:
        posts = fetch_from_subreddit(sub, score, limit=500)
        all_data.extend(posts)
    except Exception as e:
        print(f"Failed for r/{sub}: {e}")

df = pd.DataFrame(all_data)
df.to_csv("data/raw/reddit_emotions.csv", index=False)
print("Data saved to data/raw/reddit_emotions.csv")
