import unittest
from unittest.mock import patch
from agents.market_analyst import market_analyst_agent
import json

class TestMarketAnalystAgent(unittest.TestCase):

    @patch('agents.market_analyst.get_reddit_threads')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke')
    def test_market_analyst_agent(self, mock_chain_invoke, mock_get_reddit_threads):
        # Mock the get_reddit_threads tool
        mock_get_reddit_threads.return_value = [
            {"title": "Job: Software Engineer", "url": "http://test.com/1"},
            {"title": "Hiring: Python Developer", "url": "http://test.com/2"},
        ]

        # Mock the LLM response
        mock_chain_invoke.return_value = json.dumps([
            {"title": "Job: Software Engineer", "url": "http://test.com/1", "relevance_score": 0.9},
            {"title": "Hiring: Python Developer", "url": "http://test.com/2", "relevance_score": 0.8},
        ])
        
        user_profile = {
            "skills": ["Python", "Software Engineering"],
            "implied_interests": ["AI"]
        }
        
        opportunities = market_analyst_agent(user_profile)

        self.assertEqual(len(opportunities), 2)
        self.assertIn("relevance_score", opportunities[0])
        self.assertEqual(opportunities[0]["relevance_score"], 0.9)

if __name__ == "__main__":
    unittest.main()
