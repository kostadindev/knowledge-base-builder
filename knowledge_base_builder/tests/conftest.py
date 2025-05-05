import pytest
from unittest.mock import MagicMock
import os
import tempfile

@pytest.fixture
def mock_gemini_client():
    """Create a mock Gemini client for testing."""
    client = MagicMock()
    client.generate_content.return_value = "Generated content"
    return client

@pytest.fixture
def temp_pdf_file():
    """Create a temporary PDF file for testing."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(b"PDF test content")
    temp_file.close()
    
    yield temp_file.name
    
    # Clean up after test
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)

@pytest.fixture
def sample_config():
    """Provide a sample configuration dictionary."""
    return {
        'GOOGLE_API_KEY': 'fake_key',
        'GEMINI_MODEL': 'gemini-2.0-flash',
        'GEMINI_TEMPERATURE': 0.7,
        'GITHUB_USERNAME': 'test_user',
        'GITHUB_API_KEY': 'fake_github_key'
    }

@pytest.fixture
def sample_sources():
    """Provide a sample sources dictionary."""
    return {
        'pdf_urls': ['https://example.com/test.pdf', 'file:///fake/path/doc.pdf'],
        'web_urls': ['https://example.com/page1', 'https://example.com/page2'],
        'sitemap_url': 'https://example.com/sitemap.xml'
    } 