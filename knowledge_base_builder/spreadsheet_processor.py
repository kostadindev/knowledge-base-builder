import os
import requests
import tempfile
import urllib.parse
import pandas as pd
import re
import ezodf
from io import StringIO

class SpreadsheetProcessor:
    """Handle spreadsheet processing for .csv, .tsv, .xlsx, and .ods files."""
    
    @staticmethod
    def download(url: str) -> str:
        """Download a spreadsheet from a URL or load from local file."""
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
                raise Exception(f"Failed to download spreadsheet from {url}")
            
            # Parse the filename from URL or headers
            filename = url.split('/')[-1].split('?')[0]
            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                cd_match = re.findall('filename="(.+?)"', content_disposition)
                if cd_match:
                    filename = cd_match[0]
            
            # Ensure we have the correct file extension
            if not any(filename.lower().endswith(ext) for ext in ['.csv', '.tsv', '.xlsx', '.ods']):
                # Try to guess from content-type
                content_type = response.headers.get('content-type', '')
                if 'text/csv' in content_type:
                    filename = filename + '.csv'
                elif 'text/tab-separated-values' in content_type:
                    filename = filename + '.tsv'
                elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
                    filename = filename + '.xlsx'
                elif 'application/vnd.oasis.opendocument.spreadsheet' in content_type:
                    filename = filename + '.ods'
                else:
                    # Default to .csv if we can't determine
                    filename = filename + '.csv'
            
            # Create temporary file with the correct extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
            temp_file.write(response.content)
            temp_file.close()
            return temp_file.name

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from a spreadsheet file based on its extension."""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            return SpreadsheetProcessor._extract_from_csv(file_path)
        elif file_ext == '.tsv':
            return SpreadsheetProcessor._extract_from_tsv(file_path)
        elif file_ext == '.xlsx':
            return SpreadsheetProcessor._extract_from_xlsx(file_path)
        elif file_ext == '.ods':
            return SpreadsheetProcessor._extract_from_ods(file_path)
        else:
            raise ValueError(f"Unsupported spreadsheet format: {file_ext}")

    @staticmethod
    def _extract_from_csv(file_path: str) -> str:
        """Extract text from a .csv file."""
        try:
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
            return SpreadsheetProcessor._dataframe_to_markdown(df)
        except Exception as e:
            raise Exception(f"Error extracting text from .csv file: {e}")

    @staticmethod
    def _extract_from_tsv(file_path: str) -> str:
        """Extract text from a .tsv file."""
        try:
            df = pd.read_csv(file_path, sep='\t', encoding='utf-8', on_bad_lines='skip')
            return SpreadsheetProcessor._dataframe_to_markdown(df)
        except Exception as e:
            raise Exception(f"Error extracting text from .tsv file: {e}")

    @staticmethod
    def _extract_from_xlsx(file_path: str) -> str:
        """Extract text from a .xlsx file."""
        try:
            # Read all sheets
            xlsx = pd.ExcelFile(file_path)
            sheet_names = xlsx.sheet_names
            
            results = []
            for sheet_name in sheet_names:
                df = pd.read_excel(xlsx, sheet_name=sheet_name)
                if not df.empty:
                    results.append(f"## Sheet: {sheet_name}\n\n")
                    results.append(SpreadsheetProcessor._dataframe_to_markdown(df))
                    results.append("\n\n")
            
            return ''.join(results).strip()
        except Exception as e:
            raise Exception(f"Error extracting text from .xlsx file: {e}")

    @staticmethod
    def _extract_from_ods(file_path: str) -> str:
        """Extract text from a .ods file."""
        try:
            doc = ezodf.opendoc(file_path)
            results = []
            
            for sheet in doc.sheets:
                sheet_name = sheet.name
                # Convert sheet to DataFrame
                df = pd.DataFrame({col: [sheet[row, col].value for row in range(sheet.nrows())] 
                                 for col in range(sheet.ncols())})
                
                # Use first row as header if it contains string values
                if all(isinstance(val, str) for val in df.iloc[0].values):
                    df.columns = df.iloc[0]
                    df = df.iloc[1:]
                
                if not df.empty:
                    results.append(f"## Sheet: {sheet_name}\n\n")
                    results.append(SpreadsheetProcessor._dataframe_to_markdown(df))
                    results.append("\n\n")
            
            return ''.join(results).strip()
        except Exception as e:
            raise Exception(f"Error extracting text from .ods file: {e}")

    @staticmethod
    def _dataframe_to_markdown(df: pd.DataFrame) -> str:
        """Convert a pandas DataFrame to a markdown table."""
        try:
            # Handle large dataframes by sampling or truncating
            if len(df) > 100:
                # Option 1: Take a sample of the data
                # df = df.sample(n=100, random_state=42)
                
                # Option 2: Take first and last rows
                df = pd.concat([df.head(50), df.tail(50)])
            
            # Create a string buffer and write the dataframe as markdown
            buffer = StringIO()
            
            # Generate column header row with alignment
            header = "| " + " | ".join(str(col) for col in df.columns) + " |"
            separator = "| " + " | ".join(["-" * max(3, len(str(col))) for col in df.columns]) + " |"
            
            # Write to buffer
            buffer.write(header + "\n")
            buffer.write(separator + "\n")
            
            # Generate rows
            for _, row in df.iterrows():
                row_values = "| " + " | ".join(str(val).replace("\n", " ") for val in row.values) + " |"
                buffer.write(row_values + "\n")
            
            # Add summary information
            buffer.write(f"\n*Table contains {len(df)} rows and {len(df.columns)} columns.*\n")
            
            return buffer.getvalue()
        except Exception as e:
            raise Exception(f"Error converting DataFrame to markdown: {e}") 