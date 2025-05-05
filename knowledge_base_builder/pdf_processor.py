import os
import requests
import tempfile
import urllib.parse
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFProcessor:
    """Handle PDF document processing."""
    @staticmethod
    def download(url: str) -> str:
        """Download a PDF from a URL or load from local file."""
        if url.startswith("file://"):
            parsed = urllib.parse.urlparse(url)
            local_path = urllib.parse.unquote(parsed.path)
            
            # Handle path differences between Windows and Mac/Linux
            if os.name == 'nt':  # Windows
                # For Windows paths with drive letters (like C:/)
                if local_path.startswith('/') and len(local_path) > 1:
                    # Remove the leading slash before the drive letter
                    # Example: /C:/path/to/file.pdf -> C:/path/to/file.pdf
                    if local_path[1].isalpha() and local_path[2] == ':':
                        local_path = local_path[1:]
                    else:
                        local_path = local_path.lstrip('/')
            else:  # Mac/Linux - ensure path starts with /
                if not local_path.startswith('/'):
                    local_path = '/' + local_path
            
            # Replace any remaining URL encodings (like %20 for spaces)
            local_path = urllib.parse.unquote(local_path)
                    
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"Local file not found: {local_path}")
            return local_path
        else:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to download PDF from {url}")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extract text from a PDF file."""
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=100)
        chunks = splitter.split_documents(documents)
        return "\n".join(chunk.page_content for chunk in chunks) 