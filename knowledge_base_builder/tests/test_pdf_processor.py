import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):
    """Test the PDFProcessor class functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.processor = PDFProcessor()
        
        # Create a temporary file to use as a test PDF
        self.temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        self.temp_pdf.write(b"PDF test content")
        self.temp_pdf.close()
        
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_pdf.name):
            os.unlink(self.temp_pdf.name)
    
    @patch('pdf_processor.requests.get')
    def test_download_from_url(self, mock_get):
        """Test downloading a PDF from a URL."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"PDF content"
        mock_get.return_value = mock_response
        
        path = self.processor.download("http://example.com/test.pdf")
        
        self.assertTrue(os.path.exists(path))
        mock_get.assert_called_once_with("http://example.com/test.pdf")
        
        # Clean up
        os.unlink(path)
    
    @patch('pdf_processor.requests.get')
    def test_download_from_url_error(self, mock_get):
        """Test handling error when downloading from URL."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            self.processor.download("http://example.com/test.pdf")
    
    def test_download_from_local_file(self):
        """Test loading a PDF from a local file."""
        file_uri = f"file:///{self.temp_pdf.name.replace(os.path.sep, '/')}"
        
        path = self.processor.download(file_uri)
        
        # Normalize both paths before comparing
        self.assertEqual(os.path.normpath(path), os.path.normpath(self.temp_pdf.name))
    
    def test_download_from_local_file_not_found(self):
        """Test handling a missing local file."""
        file_uri = "file:///nonexistent_file.pdf"
        
        with self.assertRaises(FileNotFoundError):
            self.processor.download(file_uri)
    
    @patch('pdf_processor.PyPDFLoader')
    @patch('pdf_processor.RecursiveCharacterTextSplitter')
    def test_extract_text(self, mock_splitter, mock_loader):
        """Test extracting text from a PDF."""
        # Setup mocks
        mock_doc1 = MagicMock()
        mock_doc1.page_content = "Test page 1"
        mock_doc2 = MagicMock()
        mock_doc2.page_content = "Test page 2"
        
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_doc1, mock_doc2]
        mock_loader.return_value = mock_loader_instance
        
        mock_splitter_instance = MagicMock()
        mock_splitter_instance.split_documents.return_value = [mock_doc1, mock_doc2]
        mock_splitter.return_value = mock_splitter_instance
        
        # Call the method
        result = self.processor.extract_text(self.temp_pdf.name)
        
        # Check results
        self.assertEqual(result, "Test page 1\nTest page 2")
        mock_loader.assert_called_once_with(self.temp_pdf.name)
        mock_splitter.assert_called_once_with(chunk_size=20000, chunk_overlap=100)
        mock_splitter_instance.split_documents.assert_called_once()

if __name__ == '__main__':
    unittest.main() 