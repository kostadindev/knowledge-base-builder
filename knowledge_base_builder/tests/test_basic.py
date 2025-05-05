"""Basic tests for the Knowledge Base Builder package."""

import unittest
from unittest.mock import MagicMock, patch
from knowledge_base_builder import KBBuilder

class TestKBBuilder(unittest.TestCase):
    """Test the KBBuilder class."""
    
    @patch('knowledge_base_builder.gemini_client.ChatGoogleGenerativeAI')
    def test_initialization(self, mock_gemini):
        """Test that KBBuilder initializes correctly."""
        # Setup
        config = {
            'GOOGLE_API_KEY': 'fake-api-key',
            'GEMINI_MODEL': 'gemini-2.0-flash',
            'GEMINI_TEMPERATURE': 0.7,
        }
        
        # Execute
        kb_builder = KBBuilder(config)
        
        # Assert
        self.assertIsNotNone(kb_builder)
        self.assertEqual(kb_builder.config, config)
        self.assertIsNotNone(kb_builder.gemini_client)
        self.assertIsNotNone(kb_builder.llm)
        self.assertIsNotNone(kb_builder.pdf_processor)
        self.assertIsNotNone(kb_builder.website_processor)
        self.assertEqual(kb_builder.github_username, '')
        self.assertIsNone(kb_builder.github_processor)
        
    @patch('knowledge_base_builder.gemini_client.ChatGoogleGenerativeAI')
    def test_init_with_github(self, mock_gemini):
        """Test initialization with GitHub credentials."""
        # Setup
        config = {
            'GOOGLE_API_KEY': 'fake-api-key',
            'GEMINI_MODEL': 'gemini-2.0-flash',
            'GEMINI_TEMPERATURE': 0.7,
            'GITHUB_USERNAME': 'test-user',
            'GITHUB_API_KEY': 'fake-github-token',
        }
        
        # Execute
        kb_builder = KBBuilder(config)
        
        # Assert
        self.assertEqual(kb_builder.github_username, 'test-user')
        self.assertIsNotNone(kb_builder.github_processor)

if __name__ == '__main__':
    unittest.main()