import unittest
from unittest.mock import MagicMock, patch
from llm import LLM

class TestLLM(unittest.TestCase):
    """Test the LLM class functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.mock_client = MagicMock()
        self.llm = LLM(self.mock_client)
    
    def test_build(self):
        """Test building a knowledge base from text."""
        # Setup mock response
        self.mock_client.run.return_value = "Generated knowledge base"
        
        # Test with sample text
        result = self.llm.build("This is sample text for knowledge base generation.")
        
        # Verify response
        self.assertEqual(result, "Generated knowledge base")
        
        # Verify client was called with appropriate prompt
        self.mock_client.run.assert_called_once()
        prompt = self.mock_client.run.call_args[0][0]
        self.assertIn("This is sample text for knowledge base generation.", prompt)
        self.assertIn("Markdown knowledge base", prompt)
        self.assertIn("You're a helpful assistant", prompt)
    
    def test_recursively_merge_kbs_single(self):
        """Test merging a single knowledge base."""
        # Test with single KB
        kbs = ["Single knowledge base"]
        result = self.llm.recursively_merge_kbs(kbs)
        
        # Should return the single KB without calling run
        self.assertEqual(result, "Single knowledge base")
        self.mock_client.run.assert_not_called()
    
    def test_recursively_merge_kbs_pair(self):
        """Test merging two knowledge bases."""
        # Setup mock response
        self.mock_client.run.return_value = "Merged knowledge base"
        
        # Test with two KBs
        kbs = ["First knowledge base", "Second knowledge base"]
        result = self.llm.recursively_merge_kbs(kbs)
        
        # Verify response
        self.assertEqual(result, "Merged knowledge base")
        
        # Verify client was called once with both KBs
        self.mock_client.run.assert_called_once()
        prompt = self.mock_client.run.call_args[0][0]
        self.assertIn("First knowledge base", prompt)
        self.assertIn("Second knowledge base", prompt)
        self.assertIn("Merge", prompt)
    
    def test_recursively_merge_kbs_multiple(self):
        """Test merging multiple knowledge bases recursively."""
        # Setup mock responses for different calls
        self.mock_client.run.side_effect = [
            "Merged KB 1-2",
            "Merged KB 3-4",
            "Final merged KB"
        ]
        
        # Test with four KBs
        kbs = [
            "First knowledge base", 
            "Second knowledge base",
            "Third knowledge base",
            "Fourth knowledge base"
        ]
        result = self.llm.recursively_merge_kbs(kbs)
        
        # Verify response
        self.assertEqual(result, "Final merged KB")
        
        # Verify client was called three times
        self.assertEqual(self.mock_client.run.call_count, 3)

if __name__ == '__main__':
    unittest.main() 