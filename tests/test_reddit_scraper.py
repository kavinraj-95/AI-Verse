import unittest
from unittest.mock import patch, MagicMock
from tools.reddit_scraper import get_reddit_threads

class TestRedditScraper(unittest.TestCase):

    @patch('tools.reddit_scraper.praw.Reddit')
    def test_get_reddit_threads(self, mock_reddit):
        # Create a mock submission object
        mock_submission = MagicMock()
        mock_submission.title = "Test Thread"
        mock_submission.url = "http://test.com"
        mock_submission.subreddit.display_name = "testsubreddit"
        mock_submission.score = 10
        mock_submission.selftext = "This is a test submission."

        # Configure the mock reddit instance
        mock_instance = mock_reddit.return_value
        mock_subreddit = mock_instance.subreddit.return_value
        mock_subreddit.search.return_value = [mock_submission]

        threads = get_reddit_threads(keywords=["test"], subreddits=["testsubreddit"])

        self.assertEqual(len(threads), 1)
        self.assertEqual(threads[0]['title'], "Test Thread")
        self.assertEqual(threads[0]['url'], "http://test.com")

if __name__ == "__main__":
    unittest.main()
