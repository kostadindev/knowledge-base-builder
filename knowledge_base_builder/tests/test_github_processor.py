import unittest
from unittest.mock import patch, MagicMock
from github_processor import GitHubProcessor

class TestGitHubProcessor(unittest.TestCase):
    """Test the GitHubProcessor class functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.username = "test_user"
        self.token = "fake_token"
        self.processor = GitHubProcessor(username=self.username, token=self.token)
    
    @patch('github_processor.requests.get')
    def test_get_markdown_urls(self, mock_get):
        """Test getting markdown file URLs from GitHub repositories."""
        # Setup mock responses
        repos_response = MagicMock()
        repos_response.status_code = 200
        repos_response.json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        
        # Empty page response to terminate pagination
        empty_response = MagicMock()
        empty_response.status_code = 200
        empty_response.json.return_value = []
        
        # First repo contents
        repo1_response = MagicMock()
        repo1_response.status_code = 200
        repo1_response.json.return_value = [
            {"name": "README.md", "type": "file", "download_url": "https://raw.github.com/test_user/repo1/main/README.md"},
            {"name": "src", "type": "dir", "path": "src"},
            {"name": "test.py", "type": "file"}
        ]
        
        # Second repo contents
        repo2_response = MagicMock()
        repo2_response.status_code = 200
        repo2_response.json.return_value = [
            {"name": "README.md", "type": "file", "download_url": "https://raw.github.com/test_user/repo2/main/README.md"},
            {"name": "CONTRIBUTING.md", "type": "file", "download_url": "https://raw.github.com/test_user/repo2/main/CONTRIBUTING.md"}
        ]
        
        # Src dir contents for repo1
        src_dir_response = MagicMock()
        src_dir_response.status_code = 200
        src_dir_response.json.return_value = [
            {"name": "docs.md", "type": "file", "download_url": "https://raw.github.com/test_user/repo1/main/src/docs.md"}
        ]
        
        # Set up mock to return different responses
        mock_get.side_effect = [repos_response, empty_response, repo1_response, src_dir_response, repo2_response]
        
        # Call method
        urls = self.processor.get_markdown_urls()
        
        # Verify results
        self.assertEqual(len(urls), 4)  # Four markdown files total
        self.assertIn("https://raw.github.com/test_user/repo1/main/README.md", urls)
        self.assertIn("https://raw.github.com/test_user/repo1/main/src/docs.md", urls)
        self.assertIn("https://raw.github.com/test_user/repo2/main/README.md", urls)
        self.assertIn("https://raw.github.com/test_user/repo2/main/CONTRIBUTING.md", urls)
        
        # Verify first API call (to get repos) was made with auth header
        first_call = mock_get.call_args_list[0]
        self.assertEqual(first_call[0][0], f"https://api.github.com/users/{self.username}/repos?per_page=100&page=1")
        self.assertEqual(first_call[1]["headers"], {"Authorization": f"token {self.token}"})
    
    @patch('github_processor.requests.get')
    def test_get_markdown_urls_error(self, mock_get):
        """Test handling error when fetching repositories."""
        mock_response = MagicMock()
        mock_response.status_code = 401  # Unauthorized
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            self.processor.get_markdown_urls()
    
    @patch('github_processor.requests.get')
    def test_download_markdown(self, mock_get):
        """Test downloading markdown content."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "# Test Markdown\n\nThis is a test markdown file."
        mock_get.return_value = mock_response
        
        # Call method
        content = self.processor.download_markdown("https://raw.github.com/test_user/repo/main/README.md")
        
        # Verify results
        self.assertEqual(content, "# Test Markdown\n\nThis is a test markdown file.")
        mock_get.assert_called_once_with("https://raw.github.com/test_user/repo/main/README.md")
    
    @patch('github_processor.requests.get')
    def test_download_markdown_error(self, mock_get):
        """Test handling error when downloading markdown."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            self.processor.download_markdown("https://raw.github.com/test_user/repo/main/README.md")

if __name__ == '__main__':
    unittest.main() 