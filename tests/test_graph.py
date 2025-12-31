import unittest
from unittest.mock import patch, MagicMock, call
from graph import app, profiler_node, market_analyst_node, roadmap_planner_node, executive_agent_node, critic_reflector_node
import io

class TestGraph(unittest.TestCase):

    def test_graph_flow(self):
        # We will mock all the nodes in the graph to test the flow
        with patch('graph.profiler_agent') as mock_profiler, \
             patch('graph.market_analyst_agent') as mock_market, \
             patch('graph.roadmap_planner_agent') as mock_roadmap, \
             patch('graph.executive_agent') as mock_executive:

            # Mock return values
            mock_profiler.return_value = {"skills": ["python"]}
            mock_market.return_value = [{"title": "Python dev"}]
            mock_roadmap.return_value = "Learn FastAPI"
            
            # Let's test the nodes individually, accumulating state
            state = {"agent_logs": [], "feedback_loop_count": 0}
            file_content = io.BytesIO(b"some resume data")

            profiler_result = profiler_node(state, file_content)
            state.update(profiler_result)
            self.assertIn("user_profile", state)
            
            market_result = market_analyst_node(state)
            state.update(market_result)
            self.assertIn("opportunities", state)
            
            roadmap_result = roadmap_planner_node(state)
            state.update(roadmap_result)
            self.assertIn("roadmap", state)
            
            executive_result = executive_agent_node(state)
            state.update(executive_result)
            # This node just logs, so we check the logs
            self.assertIn("Agent: Executive Agent finished.", state['agent_logs'])


    @patch('graph.critic_reflector_agent')
    def test_critic_node(self, mock_critic):
        mock_critic.return_value = "new_skill"
        
        initial_state = {
            "user_profile": {"skills": ["python"]},
            "feedback_loop_count": 0,
            "agent_logs": []
        }
        
        result = critic_reflector_node(initial_state, "some feedback")
        
        self.assertEqual(result['priority_gap'], "new_skill")
        self.assertIn("new_skill", result['user_profile']['skills'])
        self.assertEqual(result['feedback_loop_count'], 1)


if __name__ == '__main__':
    unittest.main()