import asyncio
from typing import List, Dict, Any
import os
import urllib.parse
import time
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
        self.config = config
        self.gemini_client = GeminiClient(
            api_key=config['GOOGLE_API_KEY'],
            model=config.get('GEMINI_MODEL', 'gemini-2.0-flash'),
            temperature=float(config.get('GEMINI_TEMPERATURE', 0.7)),
            max_retries=int(config.get('GEMINI_MAX_RETRIES', 3)),
            max_concurrency=int(config.get('GEMINI_MAX_CONCURRENCY', 8)),
        )
        self.llm = LLM(self.gemini_client)
        # … same processors as before …
        self.pdf_processor = PDFProcessor()
        self.document_processor = DocumentProcessor()
        self.spreadsheet_processor = SpreadsheetProcessor()
        self.web_content_processor = WebContentProcessor()
        self.website_processor = WebsiteProcessor()
        self.github_username = config.get('GITHUB_USERNAME', '')
        self.github_processor = (
            GitHubProcessor(username=self.github_username, token=config.get('GITHUB_API_KEY'))
            if self.github_username else None
        )
        self.kbs: List[str] = []

    def build_kb(self, sources: Dict[str, Any] = None, output_file: str = "final_knowledge_base.md") -> str:
        """Synchronously run the pipeline up to merge, then dispatch async merge."""
        total_start_time = time.time()
        print("🚀 Starting Knowledge Base Builder pipeline...")
        self.kbs = []
        sources = sources or {}

        # process all your legacy or unified sources exactly as before...
        if files := sources.get('files', []):
            files_start_time = time.time()
            self.process_files(files)
            files_end_time = time.time()
            print(f"⏱️ Files processing completed in {files_end_time - files_start_time:.2f} seconds")
            
        legacy_start_time = time.time()
        self._process_legacy_sources(sources)
        legacy_end_time = time.time()
        print(f"⏱️ Legacy sources processing completed in {legacy_end_time - legacy_start_time:.2f} seconds")
        
        if sitemap := sources.get('sitemap_url'):
            sitemap_start_time = time.time()
            self.process_websites(sitemap)
            sitemap_end_time = time.time()
            print(f"⏱️ Sitemap processing completed in {sitemap_end_time - sitemap_start_time:.2f} seconds")
            
        if self.github_username:
            github_start_time = time.time()
            self.process_github()
            github_end_time = time.time()
            print(f"⏱️ GitHub processing completed in {github_end_time - github_start_time:.2f} seconds")

        # now do async merge & write file
        print("🔀 Merging all knowledge bases asynchronously...")
        merge_start_time = time.time()
        final_kb = asyncio.get_event_loop().run_until_complete(
            self.llm.recursively_merge_kbs(self.kbs)
        )
        merge_end_time = time.time()
        print(f"⏱️ Knowledge base merging completed in {merge_end_time - merge_start_time:.2f} seconds")

        write_start_time = time.time()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_kb)
        write_end_time = time.time()
        print(f"⏱️ File writing completed in {write_end_time - write_start_time:.2f} seconds")

        total_end_time = time.time()
        print(f"✅ Final KB written to: {output_file}")
        print(f"⏱️ Total processing time: {total_end_time - total_start_time:.2f} seconds")
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
                # Check if this is a local file path (not starting with http/https and containing a path separator)
                if not url.startswith(('http://', 'https://', 'file://')) and (os.path.sep in url or os.path.exists(url)):
                    # Convert local path to file:// URL format for internal processing
                    local_path = os.path.abspath(url)
                    
                    # Handle Windows paths differently
                    if os.name == 'nt':  # Windows
                        # For Windows, ensure path starts with / and replace backslashes with forward slashes
                        local_path = local_path.replace('\\', '/')
                        if local_path[1] == ':':  # Has drive letter like C:
                            url = f"file:///{local_path}"
                        else:
                            url = f"file:///{local_path}"
                    else:
                        # For Unix-like systems
                        url = f"file://{urllib.parse.quote(local_path)}"
                    
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
        start_time = time.time()
        
        download_start = time.time()
        path = self.pdf_processor.download(url)
        download_end = time.time()
        print(f"  ⏱️ Download: {download_end - download_start:.2f} seconds")
        
        extract_start = time.time()
        text = self.pdf_processor.extract_text(path)
        extract_end = time.time()
        print(f"  ⏱️ Text extraction: {extract_end - extract_start:.2f} seconds")
        
        if text.strip():
            kb_start = time.time()
            self.kbs.append(self.llm.build_kb(text))
            kb_end = time.time()
            print(f"  ⏱️ KB building: {kb_end - kb_start:.2f} seconds")
        
        end_time = time.time()
        print(f"  ⏱️ Total PDF processing: {end_time - start_time:.2f} seconds")

    def _process_document(self, url: str) -> None:
        """Process a document file."""
        print(f"📝 Document: {url}")
        start_time = time.time()
        
        download_start = time.time()
        path = self.document_processor.download(url)
        download_end = time.time()
        print(f"  ⏱️ Download: {download_end - download_start:.2f} seconds")
        
        extract_start = time.time()
        text = self.document_processor.extract_text(path)
        extract_end = time.time()
        print(f"  ⏱️ Text extraction: {extract_end - extract_start:.2f} seconds")
        
        if text.strip():
            kb_start = time.time()
            self.kbs.append(self.llm.build_kb(text))
            kb_end = time.time()
            print(f"  ⏱️ KB building: {kb_end - kb_start:.2f} seconds")
        
        end_time = time.time()
        print(f"  ⏱️ Total document processing: {end_time - start_time:.2f} seconds")

    def _process_spreadsheet(self, url: str) -> None:
        """Process a spreadsheet file."""
        print(f"📊 Spreadsheet: {url}")
        start_time = time.time()
        
        download_start = time.time()
        path = self.spreadsheet_processor.download(url)
        download_end = time.time()
        print(f"  ⏱️ Download: {download_end - download_start:.2f} seconds")
        
        extract_start = time.time()
        text = self.spreadsheet_processor.extract_text(path)
        extract_end = time.time()
        print(f"  ⏱️ Text extraction: {extract_end - extract_start:.2f} seconds")
        
        if text.strip():
            kb_start = time.time()
            self.kbs.append(self.llm.build_kb(text))
            kb_end = time.time()
            print(f"  ⏱️ KB building: {kb_end - kb_start:.2f} seconds")
        
        end_time = time.time()
        print(f"  ⏱️ Total spreadsheet processing: {end_time - start_time:.2f} seconds")

    def _process_web_content(self, url: str) -> None:
        """Process a web content file."""
        print(f"🌐 Web content: {url}")
        start_time = time.time()
        
        download_start = time.time()
        path = self.web_content_processor.download(url)
        download_end = time.time()
        print(f"  ⏱️ Download: {download_end - download_start:.2f} seconds")
        
        extract_start = time.time()
        text = self.web_content_processor.extract_text(path)
        extract_end = time.time()
        print(f"  ⏱️ Text extraction: {extract_end - extract_start:.2f} seconds")
        
        if text.strip():
            kb_start = time.time()
            self.kbs.append(self.llm.build_kb(text))
            kb_end = time.time()
            print(f"  ⏱️ KB building: {kb_end - kb_start:.2f} seconds")
        
        end_time = time.time()
        print(f"  ⏱️ Total web content processing: {end_time - start_time:.2f} seconds")

    def _process_web_url(self, url: str) -> None:
        """Process a web URL."""
        print(f"🔗 Website: {url}")
        start_time = time.time()
        
        download_start = time.time()
        text = self.website_processor.download_and_clean_html(url)
        download_end = time.time()
        print(f"  ⏱️ Download and clean: {download_end - download_start:.2f} seconds")
        
        if text.strip():
            kb_start = time.time()
            self.kbs.append(self.llm.build_kb(text))
            kb_end = time.time()
            print(f"  ⏱️ KB building: {kb_end - kb_start:.2f} seconds")
        
        end_time = time.time()
        print(f"  ⏱️ Total website processing: {end_time - start_time:.2f} seconds")

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
            sitemap_start = time.time()
            urls = self.website_processor.get_urls_from_sitemap(sitemap_url)
            sitemap_end = time.time()
            print(f"  ⏱️ Sitemap fetching: {sitemap_end - sitemap_start:.2f} seconds")
            
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
            github_start = time.time()
            md_urls = self.github_processor.get_markdown_urls()
            github_end = time.time()
            print(f"  ⏱️ GitHub URLs fetching: {github_end - github_start:.2f} seconds")
            
            for url in md_urls:
                try:
                    print(f"📘 GitHub MD: {url}")
                    url_start = time.time()
                    
                    download_start = time.time()
                    text = self.github_processor.download_markdown(url)
                    download_end = time.time()
                    print(f"  ⏱️ Markdown download: {download_end - download_start:.2f} seconds")
                    
                    if text.strip():
                        kb_start = time.time()
                        self.kbs.append(self.llm.build_kb(text))
                        kb_end = time.time()
                        print(f"  ⏱️ KB building: {kb_end - kb_start:.2f} seconds")
                    
                    url_end = time.time()
                    print(f"  ⏱️ Total GitHub markdown processing: {url_end - url_start:.2f} seconds")
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
        merge_start = time.time()
        final_kb = self.llm.recursively_merge_kbs(self.kbs)
        merge_end = time.time()
        print(f"⏱️ Merging completed in {merge_end - merge_start:.2f} seconds")

        write_start = time.time()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_kb)
        write_end = time.time()
        print(f"⏱️ File writing completed in {write_end - write_start:.2f} seconds")

        print(f"✅ Final KB written to: {output_path}") 