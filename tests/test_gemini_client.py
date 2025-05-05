import unittest
from unittest.mock import patch, MagicMock
from gemini_client import GeminiClient

class TestGeminiClient(unittest.TestCase):
    """Test the GeminiClient class functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.api_key = "fake_api_key"
        self.model = "gemini-2.0-flash"
        self.temperature = 0.7
        
    @patch('gemini_client.ChatGoogleGenerativeAI')
    def test_initialization(self, mock_chat_model):
        """Test client initialization."""
        client = GeminiClient(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature
        )
        
        # Verify model was created with the correct parameters
        mock_chat_model.assert_called_once_with(
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key
        )
        
        # Verify client properties
        self.assertEqual(client.model, mock_chat_model.return_value)
    
    @patch('gemini_client.ChatGoogleGenerativeAI')
    @patch('gemini_client.HumanMessage')
    def test_run(self, mock_human_message, mock_chat_model):
        """Test content generation."""
        # Setup mock response
        mock_message = MagicMock()
        mock_message.content = "Generated response text"
        
        mock_model = MagicMock()
        mock_model.invoke.return_value = mock_message
        mock_chat_model.return_value = mock_model
        
        mock_human_message.return_value = "Human message object"
        
        # Create client and generate content
        client = GeminiClient(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature
        )
        
        result = client.run("Test prompt")
        
        # Verify response
        self.assertEqual(result, "Generated response text")
        
        # Verify invoke was called with the prompt
        mock_human_message.assert_called_once_with(content="Test prompt")
        mock_model.invoke.assert_called_once_with(["Human message object"])

if __name__ == '__main__':
    unittest.main() 