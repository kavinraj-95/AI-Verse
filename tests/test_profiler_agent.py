import unittest
from unittest.mock import patch
from agents.profiler import profiler_agent
import io
import json

class TestProfilerAgent(unittest.TestCase):

    @patch('agents.profiler.ChatGoogleGenerativeAI')
    @patch('agents.profiler.resume_parser')
    def test_profiler_agent(self, mock_resume_parser, mock_llm):
        # Mock the resume parser
        mock_resume_parser.return_value = "dummy resume content"

        # Mock the chain
        with patch('agents.profiler.StrOutputParser') as mock_parser:
            # The chain is `prompt | llm | StrOutputParser()`
            # The result of the chain is what StrOutputParser returns from its invoke
            mock_parser_instance = mock_parser.return_value
            
            # To mock the whole chain, we can mock what the final part of the chain returns
            # when it's invoked. We can't easily mock the `|` operator.
            # Instead, let's just mock the whole chain object.
            
            # The easiest way to do this is to patch the object that the chain gets assigned to.
            # However, the chain is created and used in one line: `response = chain.invoke(...)`
            # and chain is `prompt | llm | StrOutputParser()`
            
            # Let's try to mock the llm's `invoke` method.
            # The chain is `prompt | llm | StrOutputParser()`.
            # So, `llm.invoke` will be called with the output of `prompt.invoke`.
            # And `StrOutputParser.invoke` will be called with the output of `llm.invoke`.
            
            mock_llm_instance = mock_llm.return_value
            mock_llm_instance.invoke.return_value = "should not be used" # to make sure we don't use it
            
            # Let's mock the entire `chain.invoke` call
            with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_chain_invoke:
                mock_chain_invoke.return_value = json.dumps({
                    "skills": ["Python", "LangChain"],
                    "experience": ["Software Engineer"],
                    "implied_interests": ["AI"]
                })
                
                dummy_file = io.BytesIO(b"dummy resume content")
                profile = profiler_agent(dummy_file)

                self.assertIn("skills", profile)
                self.assertEqual(profile["skills"], ["Python", "LangChain"])

if __name__ == "__main__":
    unittest.main()
