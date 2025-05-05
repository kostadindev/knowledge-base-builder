import unittest
from unittest.mock import patch, MagicMock
from website_processor import WebsiteProcessor

class TestWebsiteProcessor(unittest.TestCase):
    """Test the WebsiteProcessor class functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.processor = WebsiteProcessor()
    
    @patch('website_processor.requests.get')
    def test_get_urls_from_sitemap(self, mock_get):
        """Test extracting URLs from a sitemap XML."""
        # Create mock response with sample sitemap XML
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url><loc>https://example.com/page1</loc></url>
            <url><loc>https://example.com/page2</loc></url>
            <url><loc>https://example.com/page3</loc></url>
        </urlset>
        """
        mock_get.return_value = mock_response
        
        # Call the method
        urls = self.processor.get_urls_from_sitemap("https://example.com/sitemap.xml")
        
        # Verify results
        self.assertEqual(len(urls), 3)
        self.assertIn("https://example.com/page1", urls)
        self.assertIn("https://example.com/page2", urls)
        self.assertIn("https://example.com/page3", urls)
        mock_get.assert_called_once_with("https://example.com/sitemap.xml")
    
    @patch('website_processor.requests.get')
    def test_get_urls_from_sitemap_error(self, mock_get):
        """Test handling error when loading sitemap."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            self.processor.get_urls_from_sitemap("https://example.com/sitemap.xml")
    
    @patch('website_processor.requests.get')
    def test_download_and_clean_html(self, mock_get):
        """Test downloading and cleaning HTML content."""
        # Create mock response with sample HTML
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head>
                <title>Test Page</title>
                <style>body { color: red; }</style>
                <script>console.log('test');</script>
            </head>
            <body>
                <h1>Test Header</h1>
                <p>Test paragraph</p>
                <noscript>JavaScript is disabled</noscript>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        # Call the method
        text = self.processor.download_and_clean_html("https://example.com/page")
        
        # Verify results - should contain content but not scripts, styles, etc.
        self.assertIn("Test Header", text)
        self.assertIn("Test paragraph", text)
        self.assertNotIn("JavaScript is disabled", text)
        self.assertNotIn("console.log", text)
        self.assertNotIn("color: red", text)
        mock_get.assert_called_once_with("https://example.com/page")
    
    @patch('website_processor.requests.get')
    def test_download_and_clean_html_error(self, mock_get):
        """Test handling error when downloading HTML."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            self.processor.download_and_clean_html("https://example.com/page")

if __name__ == '__main__':
    unittest.main() 