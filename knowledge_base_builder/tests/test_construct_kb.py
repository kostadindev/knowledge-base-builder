import unittest
from unittest.mock import patch, MagicMock, Mock
import os
import sys
from importlib import reload

class TestConstructKB(unittest.TestCase):
    """Test the main construct_kb script functionality."""
    
    @patch('construct_kb.KBBuilder')
    @patch('construct_kb.os.getenv')
    def test_main_function(self, mock_getenv, mock_kbb):
        """Test the main function loads environment variables and calls the KB builder."""
        # Setup mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'GOOGLE_API_KEY': 'fake_google_key',
            'GEMINI_MODEL': 'gemini-2.0-flash',
            'GEMINI_TEMPERATURE': '0.7',
            'GITHUB_USERNAME': 'test_user',
            'GITHUB_API_KEY': 'fake_github_key'
        }.get(key, default)
        
        # Setup mock KBBuilder
        mock_kbb_instance = MagicMock()
        mock_kbb.return_value = mock_kbb_instance
        
        # Call main function
        import construct_kb
        construct_kb.main()
        
        # Verify KBBuilder was initialized with the right config
        mock_kbb.assert_called_once()
        call_args = mock_kbb.call_args[0][0]
        
        self.assertEqual(call_args['GOOGLE_API_KEY'], 'fake_google_key')
        self.assertEqual(call_args['GEMINI_MODEL'], 'gemini-2.0-flash')
        self.assertEqual(call_args['GEMINI_TEMPERATURE'], 0.7)
        self.assertEqual(call_args['GITHUB_USERNAME'], 'test_user')
        self.assertEqual(call_args['GITHUB_API_KEY'], 'fake_github_key')
        
        # Verify build_kb was called with the right sources and output file
        mock_kbb_instance.build_kb.assert_called_once()
        sources_arg = mock_kbb_instance.build_kb.call_args[1]['sources']
        output_arg = mock_kbb_instance.build_kb.call_args[1]['output_file']
        
        # Check sources structure
        self.assertIn('pdf_urls', sources_arg)
        self.assertIn('web_urls', sources_arg)
        self.assertIn('sitemap_url', sources_arg)
        
        # Check output file
        self.assertEqual(output_arg, 'final_knowledge_base.md')
    
    @patch('dotenv.load_dotenv')
    def test_load_env_variables(self, mock_load_dotenv):
        """Test that the script loads environment variables at module import."""
        # Force a reload of the module to trigger the module-level code
        import sys
        if 'construct_kb' in sys.modules:
            del sys.modules['construct_kb']
            
        # Import module which will execute the module-level code
        with patch('os.getenv', return_value='dummy_value'):
            with patch('kb_builder.KBBuilder'):  # Mock KBBuilder to prevent errors
                import construct_kb
        
        # Verify load_dotenv was called
        mock_load_dotenv.assert_called_once()

if __name__ == '__main__':
    unittest.main() 