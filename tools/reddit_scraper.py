import praw
import os
from dotenv import load_dotenv

load_dotenv()

def get_reddit_threads(keywords: list[str], subreddits: list[str] = None):
    """
    Searches for relevant threads on Reddit.

    Args:
        keywords: A list of keywords to search for.
        subreddits: A list of subreddits to search in. Defaults to a predefined list.

    Returns:
        A list of dictionaries, where each dictionary represents a thread.
    """
    if subreddits is None:
        subreddits = ["forhire", "jobbit", "cscareerquestions"]

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )

    threads = []
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for keyword in keywords:
            for submission in subreddit.search(keyword, sort="new", limit=10):
                threads.append(
                    {
                        "title": submission.title,
                        "url": submission.url,
                        "subreddit": subreddit_name,
                        "score": submission.score,
                        "selftext": submission.selftext,
                    }
                )
    return threads

