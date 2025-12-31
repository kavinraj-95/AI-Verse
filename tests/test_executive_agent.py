import unittest
from unittest.mock import patch, mock_open
from agents.executive_agent import executive_agent
import json

class TestExecutiveAgent(unittest.TestCase):

    @patch('agents.executive_agent.ChatGoogleGenerativeAI')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke')
    def test_executive_agent(self, mock_chain_invoke, mock_llm):
        # Mock the LLM response
        mock_chain_invoke.return_value = "This is a draft message."

        user_profile = {"skills": ["Python"]}
        opportunity = {"title": "Python Developer"}
        
        # Mock the open function to avoid writing to a file
        with patch('builtins.open', mock_open()) as mock_file:
            draft_message = executive_agent(user_profile, opportunity)

            self.assertEqual(draft_message, "This is a draft message.")
            mock_file.assert_called_with("application_logs.json", "a")
            handle = mock_file()
            
            # Get the first call's arguments
            written_data = handle.write.call_args[0][0]
            
            # The data is a JSON string, so parse it
            log_entry = json.loads(written_data)

            self.assertEqual(log_entry['opportunity'], opportunity)
            self.assertEqual(log_entry['draft_message'], "This is a draft message.")


if __name__ == "__main__":
    unittest.main()
