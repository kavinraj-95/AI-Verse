import unittest
from unittest.mock import patch
from agents.critic_reflector import critic_reflector_agent

class TestCriticReflectorAgent(unittest.TestCase):

    @patch('agents.critic_reflector.ChatGoogleGenerativeAI')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke')
    def test_critic_reflector_agent(self, mock_chain_invoke, mock_llm):
        # Mock the LLM response
        mock_chain_invoke.return_value = "Missing AWS experience"

        rejection_feedback = "Thank you for your application, but we are looking for someone with more AWS experience."
        
        priority_gap = critic_reflector_agent(rejection_feedback)

        self.assertEqual(priority_gap, "Missing AWS experience")

if __name__ == "__main__":
    unittest.main()
