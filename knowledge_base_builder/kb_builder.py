from typing import List, Dict, Any
import os
import urllib.parse
from knowledge_base_builder.gemini_client import GeminiClient
from knowledge_base_builder.llm import LLM
from knowledge_base_builder.pdf_processor import PDFProcessor
from knowledge_base_builder.document_processor import DocumentProcessor
from knowledge_base_builder.spreadsheet_processor import SpreadsheetProcessor
from knowledge_base_builder.web_content_processor import WebContentProcessor
from knowledge_base_builder.website_processor import WebsiteProcessor
from knowledge_base_builder.github_processor import GitHubProcessor

class KBBuilder:
    """Main application class for building knowledge bases from various sources."""
    def __init__(self, config: Dict[str, Any]):
        """Initialize with API keys and model configuration."""
        # Store only API and model configuration
        self.config = config
        
        # Initialize clients
        self.gemini_client = GeminiClient(
            api_key=config['GOOGLE_API_KEY'],
            model=config.get('GEMINI_MODEL', 'gemini-2.0-flash'),
            temperature=float(config.get('GEMINI_TEMPERATURE', 0.7))
        )
        
        # Initialize processors
        self.llm = LLM(self.gemini_client)
        self.pdf_processor = PDFProcessor()
        self.document_processor = DocumentProcessor()
        self.spreadsheet_processor = SpreadsheetProcessor()
        self.web_content_processor = WebContentProcessor()
        self.website_processor = WebsiteProcessor()
        
        # Setup GitHub processor if username is provided
        self.github_username = config.get('GITHUB_USERNAME', '')
        self.github_api_key = config.get('GITHUB_API_KEY')
        if self.github_username:
            self.github_processor = GitHubProcessor(
                username=self.github_username,
                token=self.github_api_key
            )
        else:
            self.github_processor = None
            
        self.kbs = []

    def build_kb(self, sources: Dict[str, Any] = None, output_file: str = "final_knowledge_base.md") -> None:
        """Run the complete knowledge base building pipeline with provided sources and output file.
        
        Args:
            sources: Dictionary containing source configurations (files, sitemap_url)
            output_file: Path to the output knowledge base file
        """
        print("🚀 Starting Knowledge Base Builder pipeline...")
        
        # Clear any previous knowledge bases
        self.kbs = []
        
        # Use empty dict if no sources provided
        sources = sources or {}
        
        # Process all files (unified approach)
        files = sources.get('files', [])
        if files:
            print(f"📂 Processing {len(files)} files/URLs...")
            self.process_files(files)
        
        # For backward compatibility
        self._process_legacy_sources(sources)
        
        # Process websites from sitemap
        sitemap_url = sources.get('sitemap_url')
        if sitemap_url:
            print(f"🔍 Processing sitemap: {sitemap_url}")
            self.process_websites(sitemap_url)
        
        # Process GitHub repositories if username is provided
        if self.github_username:
            print(f"📦 Processing GitHub repositories for user: {self.github_username}")
            self.process_github()
        
        # Build the final knowledge base
        self.build_final_kb(output_file)
        
        print("✅ Knowledge Base Builder pipeline completed successfully!")
        return output_file
    
    def _process_legacy_sources(self, sources: Dict[str, Any]) -> None:
        """Process legacy source format for backward compatibility."""
        # Process PDFs
        pdf_urls = sources.get('pdf_urls', [])
        if pdf_urls:
            print(f"📄 Processing {len(pdf_urls)} PDF documents (legacy format)...")
            self.process_pdfs(pdf_urls)
        
        # Process documents
        document_urls = sources.get('document_urls', [])
        if document_urls:
            print(f"📝 Processing {len(document_urls)} documents (legacy format)...")
            self.process_documents(document_urls)
        
        # Process spreadsheets
        spreadsheet_urls = sources.get('spreadsheet_urls', [])
        if spreadsheet_urls:
            print(f"📊 Processing {len(spreadsheet_urls)} spreadsheets (legacy format)...")
            self.process_spreadsheets(spreadsheet_urls)
        
        # Process web content files
        web_content_urls = sources.get('web_content_urls', [])
        if web_content_urls:
            print(f"🌐 Processing {len(web_content_urls)} web content files (legacy format)...")
            self.process_web_content(web_content_urls)
        
        # Process individual web URLs
        web_urls = sources.get('web_urls', [])
        if web_urls:
            print(f"🌐 Processing {len(web_urls)} individual web pages (legacy format)...")
            self.process_web_urls(web_urls)

    def process_files(self, files: List[str]) -> None:
        """Process files and URLs automatically based on their type."""
        for url in files:
            try:
                # Determine if this is a web URL or file path
                if url.startswith(('http://', 'https://')) and not any(url.lower().endswith(ext) for ext in 
                                                                   ['.pdf', '.docx', '.txt', '.md', '.rtf', 
                                                                    '.csv', '.tsv', '.xlsx', '.ods',
                                                                    '.html', '.xml', '.json', '.yaml', '.yml']):
                    # Handle as a web URL
                    self._process_web_url(url)
                else:
                    # Handle based on file extension
                    file_ext = os.path.splitext(url)[1].lower()
                    
                    if file_ext == '.pdf':
                        self._process_pdf(url)
                    elif file_ext in ['.docx', '.txt', '.md', '.rtf']:
                        self._process_document(url)
                    elif file_ext in ['.csv', '.tsv', '.xlsx', '.ods']:
                        self._process_spreadsheet(url)
                    elif file_ext in ['.html', '.xml', '.json', '.yaml', '.yml']:
                        self._process_web_content(url)
                    else:
                        # Try to process as a web URL if extension is unknown
                        self._process_web_url(url)
            except Exception as e:
                print(f"❌ Error processing file: {url} - {e}")

    def _process_pdf(self, url: str) -> None:
        """Process a PDF file."""
        print(f"📄 PDF: {url}")
        path = self.pdf_processor.download(url)
        text = self.pdf_processor.extract_text(path)
        if text.strip():
            self.kbs.append(self.llm.build_kb(text))

    def _process_document(self, url: str) -> None:
        """Process a document file."""
        print(f"📝 Document: {url}")
        path = self.document_processor.download(url)
        text = self.document_processor.extract_text(path)
        if text.strip():
            self.kbs.append(self.llm.build_kb(text))

    def _process_spreadsheet(self, url: str) -> None:
        """Process a spreadsheet file."""
        print(f"📊 Spreadsheet: {url}")
        path = self.spreadsheet_processor.download(url)
        text = self.spreadsheet_processor.extract_text(path)
        if text.strip():
            self.kbs.append(self.llm.build_kb(text))

    def _process_web_content(self, url: str) -> None:
        """Process a web content file."""
        print(f"🌐 Web content: {url}")
        path = self.web_content_processor.download(url)
        text = self.web_content_processor.extract_text(path)
        if text.strip():
            self.kbs.append(self.llm.build_kb(text))

    def _process_web_url(self, url: str) -> None:
        """Process a web URL."""
        print(f"🔗 Website: {url}")
        text = self.website_processor.download_and_clean_html(url)
        if text.strip():
            self.kbs.append(self.llm.build_kb(text))

    def process_pdfs(self, pdf_urls: List[str]) -> None:
        """Process and build knowledge bases from PDFs."""
        for url in pdf_urls:
            try:
                self._process_pdf(url)
            except Exception as e:
                print(f"❌ PDF error: {e}")

    def process_documents(self, document_urls: List[str]) -> None:
        """Process and build knowledge bases from documents (.docx, .txt, .md, .rtf)."""
        for url in document_urls:
            try:
                self._process_document(url)
            except Exception as e:
                print(f"❌ Document error: {e}")

    def process_spreadsheets(self, spreadsheet_urls: List[str]) -> None:
        """Process and build knowledge bases from spreadsheets (.csv, .tsv, .xlsx, .ods)."""
        for url in spreadsheet_urls:
            try:
                self._process_spreadsheet(url)
            except Exception as e:
                print(f"❌ Spreadsheet error: {e}")

    def process_web_content(self, web_content_urls: List[str]) -> None:
        """Process and build knowledge bases from web content files (.html, .xml, .json, .yaml/.yml)."""
        for url in web_content_urls:
            try:
                self._process_web_content(url)
            except Exception as e:
                print(f"❌ Web content error: {e}")

    def process_web_urls(self, web_urls: List[str]) -> None:
        """Process and build knowledge bases from individual web URLs."""
        for url in web_urls:
            try:
                self._process_web_url(url)
            except Exception as e:
                print(f"❌ Website error: {e}")

    def process_websites(self, sitemap_url: str) -> None:
        """Process and build knowledge bases from websites."""
        try:
            print(f"🌐 Sitemap: {sitemap_url}")
            urls = self.website_processor.get_urls_from_sitemap(sitemap_url)
            for url in urls:
                try:
                    self._process_web_url(url)
                except Exception as e:
                    print(f"❌ Site error: {e}")
        except Exception as e:
            print(f"❌ Sitemap load error: {e}")

    def process_github(self) -> None:
        """Process and build knowledge bases from GitHub markdown files."""
        if not self.github_processor:
            print("⚠️ GitHub processing skipped - no username provided")
            return
            
        try:
            md_urls = self.github_processor.get_markdown_urls()
            for url in md_urls:
                try:
                    print(f"📘 GitHub MD: {url}")
                    text = self.github_processor.download_markdown(url)
                    if text.strip():
                        self.kbs.append(self.llm.build_kb(text))
                except Exception as e:
                    print(f"❌ GitHub MD error: {e}")
        except Exception as e:
            print(f"❌ GitHub fetch error: {e}")

    def build_final_kb(self, output_path: str = "final_knowledge_base.md") -> None:
        """Build and save the final knowledge base."""
        if not self.kbs:
            print("⚠️ No knowledge bases created.")
            return

        print("🔀 Merging all knowledge bases...")
        final_kb = self.llm.recursively_merge_kbs(self.kbs)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_kb)

        print(f"✅ Final KB written to: {output_path}") 