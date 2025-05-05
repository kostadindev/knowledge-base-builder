import unittest
from unittest.mock import MagicMock, patch
from kb_builder import KBBuilder

class TestKBBuilder(unittest.TestCase):
    """Test the KBBuilder class functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.config = {
            'GOOGLE_API_KEY': 'fake_key',
            'GEMINI_MODEL': 'gemini-2.0-flash',
            'GEMINI_TEMPERATURE': 0.7,
            'GITHUB_USERNAME': 'test_user',
            'GITHUB_API_KEY': 'fake_github_key'
        }
    
    @patch('kb_builder.GeminiClient')
    @patch('kb_builder.LLM')
    @patch('kb_builder.PDFProcessor')
    @patch('kb_builder.WebsiteProcessor')
    @patch('kb_builder.GitHubProcessor')
    def test_init(self, mock_github, mock_web, mock_pdf, mock_llm, mock_gemini):
        """Test that KBBuilder initializes with the correct configuration."""
        kbb = KBBuilder(self.config)
        
        # Verify client initialization
        mock_gemini.assert_called_once()
        mock_llm.assert_called_once()
        mock_pdf.assert_called_once()
        mock_web.assert_called_once()
        mock_github.assert_called_once()
        
        self.assertEqual(kbb.github_username, 'test_user')
    
    @patch('kb_builder.GeminiClient')
    def test_init_without_github(self, mock_gemini):
        """Test initialization without GitHub credentials."""
        config = self.config.copy()
        config['GITHUB_USERNAME'] = ''
        
        kbb = KBBuilder(config)
        self.assertIsNone(kbb.github_processor)
    
    @patch('kb_builder.KBBuilder.process_pdfs')
    @patch('kb_builder.KBBuilder.process_web_urls')
    @patch('kb_builder.KBBuilder.process_websites')
    @patch('kb_builder.KBBuilder.process_github')
    @patch('kb_builder.KBBuilder.build_final_kb')
    def test_build_kb(self, mock_final, mock_github, mock_web, mock_urls, mock_pdfs):
        """Test the build_kb method calls all expected processing functions."""
        with patch('kb_builder.GeminiClient'):
            kbb = KBBuilder(self.config)
            
            sources = {
                'pdf_urls': ['test.pdf'],
                'web_urls': ['http://test.com'],
                'sitemap_url': 'http://test.com/sitemap.xml'
            }
            
            kbb.build_kb(sources, 'test_output.md')
            
            mock_pdfs.assert_called_once_with(['test.pdf'])
            mock_urls.assert_called_once_with(['http://test.com'])
            mock_web.assert_called_once_with('http://test.com/sitemap.xml')
            mock_github.assert_called_once()
            mock_final.assert_called_once_with('test_output.md')
    
    @patch('kb_builder.KBBuilder.build_final_kb')
    def test_build_kb_empty_sources(self, mock_final):
        """Test build_kb with empty sources."""
        with patch('kb_builder.GeminiClient'):
            kbb = KBBuilder(self.config)
            kbb.build_kb({}, 'test_output.md')
            
            # Final KB should still be built
            mock_final.assert_called_once_with('test_output.md')

if __name__ == '__main__':
    unittest.main() 