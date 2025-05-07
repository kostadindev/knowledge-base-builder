import os
import requests
import tempfile
import urllib.parse
import re
import json
import yaml
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from knowledge_base_builder.base_processor import BaseProcessor

class WebContentProcessor(BaseProcessor):
    """Handle web content processing for .html, .xml, .json, and .yaml/.yml files."""
    
    SUPPORTED_EXTENSIONS = ['.html', '.xml', '.json', '.yaml', '.yml']
    
    @staticmethod
    def download(url: str) -> str:
        """Download web content from a URL or load from local file."""
        return BaseProcessor.download(url, WebContentProcessor.SUPPORTED_EXTENSIONS)

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
                data = json.load(file)
            
            # Convert JSON to a structured text representation
            def format_json(obj, level=0):
                if isinstance(obj, dict):
                    result = []
                    for key, value in obj.items():
                        indent = '  ' * level
                        if isinstance(value, (dict, list)):
                            result.append(f"{indent}{key}:")
                            result.extend(format_json(value, level + 1))
                        else:
                            result.append(f"{indent}{key}: {value}")
                    return result
                elif isinstance(obj, list):
                    result = []
                    for item in obj:
                        if isinstance(item, (dict, list)):
                            result.extend(format_json(item, level))
                        else:
                            result.append('  ' * level + str(item))
                    return result
                else:
                    return ['  ' * level + str(obj)]
            
            text_lines = format_json(data)
            return '\n'.join(text_lines)
        except Exception as e:
            raise Exception(f"Error extracting text from .json file: {e}")

    @staticmethod
    def _extract_from_yaml(file_path: str) -> str:
        """Extract text from a .yaml/.yml file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                data = yaml.safe_load(file)
            
            # Convert YAML to a structured text representation
            def format_yaml(obj, level=0):
                if isinstance(obj, dict):
                    result = []
                    for key, value in obj.items():
                        indent = '  ' * level
                        if isinstance(value, (dict, list)):
                            result.append(f"{indent}{key}:")
                            result.extend(format_yaml(value, level + 1))
                        else:
                            result.append(f"{indent}{key}: {value}")
                    return result
                elif isinstance(obj, list):
                    result = []
                    for item in obj:
                        if isinstance(item, (dict, list)):
                            result.extend(format_yaml(item, level))
                        else:
                            result.append('  ' * level + f"- {item}")
                    return result
                else:
                    return ['  ' * level + str(obj)]
            
            text_lines = format_yaml(data)
            return '\n'.join(text_lines)
        except Exception as e:
            raise Exception(f"Error extracting text from .yaml/.yml file: {e}") 