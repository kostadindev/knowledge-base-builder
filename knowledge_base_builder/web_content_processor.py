import os
import requests
import tempfile
import urllib.parse
import re
import json
import yaml
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class WebContentProcessor:
    """Handle web content processing for .html, .xml, .json, and .yaml/.yml files."""
    
    @staticmethod
    def download(url: str) -> str:
        """Download web content from a URL or load from local file."""
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
                raise Exception(f"Failed to download web content from {url}")
            
            # Parse the filename from URL or headers
            filename = url.split('/')[-1].split('?')[0]
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                cd_match = re.findall('filename="(.+?)"', content_disposition)
                if cd_match:
                    filename = cd_match[0]
            
            # Ensure we have the correct file extension
            if not any(filename.lower().endswith(ext) for ext in ['.html', '.xml', '.json', '.yaml', '.yml']):
                # Try to guess from content-type
                content_type = response.headers.get('content-type', '')
                if 'text/html' in content_type:
                    filename = filename + '.html'
                elif 'application/xml' in content_type or 'text/xml' in content_type:
                    filename = filename + '.xml'
                elif 'application/json' in content_type:
                    filename = filename + '.json'
                elif 'application/yaml' in content_type or 'text/yaml' in content_type:
                    filename = filename + '.yaml'
                else:
                    # Attempt to detect format from content
                    content = response.text
                    if content.strip().startswith(('<', '<!', '<?')):
                        # Likely HTML or XML
                        if '<html' in content.lower():
                            filename = filename + '.html'
                        else:
                            filename = filename + '.xml'
                    elif content.strip().startswith('{') and content.strip().endswith('}'):
                        # Likely JSON
                        filename = filename + '.json'
                    elif ':' in content and '\n' in content:
                        # Possibly YAML
                        filename = filename + '.yaml'
                    else:
                        # Default to HTML
                        filename = filename + '.html'
            
            # Create temporary file with the correct extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from a web content file based on its extension."""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.html':
            return WebContentProcessor._extract_from_html(file_path)
        elif file_ext == '.xml':
            return WebContentProcessor._extract_from_xml(file_path)
        elif file_ext == '.json':
            return WebContentProcessor._extract_from_json(file_path)
        elif file_ext in ['.yaml', '.yml']:
            return WebContentProcessor._extract_from_yaml(file_path)
        else:
            raise ValueError(f"Unsupported web content format: {file_ext}")

    @staticmethod
    def _extract_from_html(file_path: str) -> str:
        """Extract text from an .html file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                html_content = file.read()
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "meta", "link", "svg", "path"]):
                script.extract()
            
            # Get text
            text = soup.get_text(separator=' ')
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines)
            
            # Remove excessive newlines and whitespace
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'\s{2,}', ' ', text)
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from .html file: {e}")

    @staticmethod
    def _extract_from_xml(file_path: str) -> str:
        """Extract text from an .xml file."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Convert XML to a structured text representation
            def format_element(element, level=0):
                result = []
                indent = '  ' * level
                
                # Element tag with attributes
                attrs = ' '.join([f'{k}="{v}"' for k, v in element.attrib.items()])
                tag_line = f"{indent}{element.tag}"
                if attrs:
                    tag_line += f" [{attrs}]"
                result.append(tag_line)
                
                # Element text content (if any)
                if element.text and element.text.strip():
                    result.append(f"{indent}  {element.text.strip()}")
                
                # Process child elements
                for child in element:
                    result.extend(format_element(child, level + 1))
                    
                return result
            
            text_lines = format_element(root)
            return '\n'.join(text_lines)
        except Exception as e:
            # Fall back to raw content if parsing fails
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    return file.read()
            except:
                raise Exception(f"Error extracting text from .xml file: {e}")

    @staticmethod
    def _extract_from_json(file_path: str) -> str:
        """Extract text from a .json file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                json_data = json.load(file)
            
            # Format JSON as markdown
            markdown = ["# JSON Content\n"]
            
            def process_json(data, prefix="", level=0):
                result = []
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, (dict, list)) and value:
                            result.append(f"{'#' * (level + 2)} {prefix}{key}")
                            result.extend(process_json(value, "", level + 1))
                        else:
                            result.append(f"- **{key}**: {value}")
                elif isinstance(data, list):
                    for i, item in enumerate(data):
                        if isinstance(item, (dict, list)) and item:
                            if len(data) > 10 and i >= 5 and i < len(data) - 5:
                                if i == 5:
                                    result.append(f"- *... {len(data) - 10} more items ...*")
                                continue
                            result.append(f"### Item {i+1}")
                            result.extend(process_json(item, "", level + 1))
                        else:
                            result.append(f"- {item}")
                else:
                    result.append(str(data))
                
                return result
            
            formatted_text = process_json(json_data, level=1)
            markdown.extend(formatted_text)
            
            return '\n'.join(markdown)
        except Exception as e:
            # Fall back to raw content if parsing fails
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    return file.read()
            except:
                raise Exception(f"Error extracting text from .json file: {e}")

    @staticmethod
    def _extract_from_yaml(file_path: str) -> str:
        """Extract text from a .yaml or .yml file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                yaml_data = yaml.safe_load(file)
            
            # Convert to JSON and use the same formatting function
            return WebContentProcessor._format_yaml_as_markdown(yaml_data)
        except Exception as e:
            # Fall back to raw content if parsing fails
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    return file.read()
            except:
                raise Exception(f"Error extracting text from YAML file: {e}")
    
    @staticmethod
    def _format_yaml_as_markdown(data, level=1):
        """Format YAML data as markdown."""
        markdown = ["# YAML Content\n"]
        
        def process_yaml(data, prefix="", level=0):
            result = []
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)) and value:
                        result.append(f"{'#' * (level + 2)} {prefix}{key}")
                        result.extend(process_yaml(value, "", level + 1))
                    else:
                        result.append(f"- **{key}**: {value}")
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, (dict, list)) and item:
                        if len(data) > 10 and i >= 5 and i < len(data) - 5:
                            if i == 5:
                                result.append(f"- *... {len(data) - 10} more items ...*")
                            continue
                        result.append(f"### Item {i+1}")
                        result.extend(process_yaml(item, "", level + 1))
                    else:
                        result.append(f"- {item}")
            else:
                result.append(str(data))
            
            return result
        
        formatted_text = process_yaml(data, level=level)
        markdown.extend(formatted_text)
        
        return '\n'.join(markdown) 