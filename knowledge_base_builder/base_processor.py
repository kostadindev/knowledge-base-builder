import os
import requests
import tempfile
import urllib.parse
import re
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """Base class for all document processors."""
    
    @staticmethod
    def download(url: str, supported_extensions: list) -> str:
        """Download a file from a URL or load from local file."""
        if url.startswith("file://"):
            parsed = urllib.parse.urlparse(url)
            local_path = urllib.parse.unquote(parsed.path)
            
            # Handle path differences between Windows and Mac/Linux
            if os.name == 'nt':  # Windows
                # For Windows paths with drive letters (like C:/)
                if local_path.startswith('/') and len(local_path) > 1:
                    # Windows paths might have multiple leading slashes - remove them all before the drive letter
                    while local_path.startswith('/') and len(local_path) > 2 and local_path[1:3] != ':/':
                        local_path = local_path[1:]
                    
                    # Now handle the format /C:/path/to/file.pdf -> C:/path/to/file.pdf
                    if len(local_path) > 2 and local_path[1].isalpha() and local_path[2] == ':':
                        local_path = local_path[1:]
                
                # Ensure proper slash direction for Windows
                local_path = local_path.replace('/', '\\')
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
                raise Exception(f"Failed to download file from {url}")
            
            # Parse the filename from URL or headers
            filename = url.split('/')[-1].split('?')[0]
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                cd_match = re.findall('filename="(.+?)"', content_disposition)
                if cd_match:
                    filename = cd_match[0]
            
            # Ensure we have the correct file extension
            if not any(filename.lower().endswith(ext) for ext in supported_extensions):
                # Try to guess from content-type
                content_type = response.headers.get('content-type', '')
                # Default to first supported extension if we can't determine
                filename = filename + supported_extensions[0]
            
            # Create temporary file with the correct extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name

    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract text from a file. Must be implemented by subclasses."""
        pass 