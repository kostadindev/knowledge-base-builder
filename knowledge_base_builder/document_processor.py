import os
import requests
import tempfile
import urllib.parse
from docx import Document
import markdown
import mistune
import re
from striprtf.striprtf import rtf_to_text
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """Handle document processing for .docx, .txt, .md, and .rtf files."""
    
    @staticmethod
    def download(url: str) -> str:
        """Download a document from a URL or load from local file."""
        if url.startswith("file://"):
            parsed = urllib.parse.urlparse(url)
            local_path = urllib.parse.unquote(parsed.path)
            
            # Handle path differences between Windows and Mac/Linux
            if os.name == 'nt':  # Windows
                # For Windows paths with drive letters (like C:/)
                if local_path.startswith('/') and len(local_path) > 1:
                    # Remove the leading slash before the drive letter
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
                raise Exception(f"Failed to download document from {url}")
            
            # Parse the filename from URL or headers
            filename = url.split('/')[-1].split('?')[0]
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                cd_match = re.findall('filename="(.+?)"', content_disposition)
                if cd_match:
                    filename = cd_match[0]
            
            # Ensure we have the correct file extension
            if not any(filename.lower().endswith(ext) for ext in ['.docx', '.txt', '.md', '.rtf']):
                # Try to guess from content-type
                content_type = response.headers.get('content-type', '')
                if 'officedocument.wordprocessingml' in content_type:
                    filename = filename + '.docx'
                elif 'text/plain' in content_type:
                    filename = filename + '.txt'
                elif 'text/markdown' in content_type:
                    filename = filename + '.md'
                elif 'application/rtf' in content_type or 'text/rtf' in content_type:
                    filename = filename + '.rtf'
                else:
                    # Default to .txt if we can't determine
                    filename = filename + '.txt'
            
            # Create temporary file with the correct extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from document file based on its extension."""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.docx':
            return DocumentProcessor._extract_from_docx(file_path)
        elif file_ext == '.txt':
            return DocumentProcessor._extract_from_txt(file_path)
        elif file_ext == '.md':
            return DocumentProcessor._extract_from_md(file_path)
        elif file_ext == '.rtf':
            return DocumentProcessor._extract_from_rtf(file_path)
        else:
            raise ValueError(f"Unsupported document format: {file_ext}")

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from a .docx file."""
        try:
            doc = Document(file_path)
            text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from .docx file: {e}")

    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from a .txt file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error extracting text from .txt file: {e}")

    @staticmethod
    def _extract_from_md(file_path: str) -> str:
        """Extract text from a .md file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                md_content = file.read()
                
            # Option 1: Return raw markdown (often best for LLM processing)
            return md_content
            
            # Option 2: Convert to HTML and strip tags (uncomment if needed)
            # html = markdown.markdown(md_content)
            # text = re.sub('<[^<]+?>', '', html)
            # return text
        except Exception as e:
            raise Exception(f"Error extracting text from .md file: {e}")

    @staticmethod
    def _extract_from_rtf(file_path: str) -> str:
        """Extract text from a .rtf file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                rtf_content = file.read()
                
            text = rtf_to_text(rtf_content)
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from .rtf file: {e}") 