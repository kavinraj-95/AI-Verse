import unittest
from unittest.mock import patch
from agents.roadmap_planner import roadmap_planner_agent

class TestRoadmapPlannerAgent(unittest.TestCase):

    @patch('agents.roadmap_planner.ChatGoogleGenerativeAI')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke')
    def test_roadmap_planner_agent(self, mock_chain_invoke, mock_llm):
        # Mock the LLM response
        mock_chain_invoke.return_value = "## Learning Roadmap\n\n### Short Term\n- Learn FastAPI"

        user_profile = {"skills": ["Python"]}
        opportunities = [{"title": "Python Developer", "selftext": "Requires FastAPI"}]
        
        roadmap = roadmap_planner_agent(user_profile, opportunities)

        self.assertIn("Learning Roadmap", roadmap)
        self.assertIn("FastAPI", roadmap)

if __name__ == "__main__":
    unittest.main()