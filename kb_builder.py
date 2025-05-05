from typing import List, Dict, Any
import os
from gemini_client import GeminiClient
from llm import LLM
from pdf_processor import PDFProcessor
from website_processor import WebsiteProcessor
from github_processor import GitHubProcessor

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
            sources: Dictionary containing source configurations (pdf_urls, web_urls, sitemap_url)
            output_file: Path to the output knowledge base file
        """
        print("🚀 Starting Knowledge Base Builder pipeline...")
        
        # Clear any previous knowledge bases
        self.kbs = []
        
        # Use empty dict if no sources provided
        sources = sources or {}
        
        # Process PDFs
        pdf_urls = sources.get('pdf_urls', [])
        if pdf_urls:
            print(f"📄 Processing {len(pdf_urls)} PDF documents...")
            self.process_pdfs(pdf_urls)
        
        # Process individual web URLs
        web_urls = sources.get('web_urls', [])
        if web_urls:
            print(f"🌐 Processing {len(web_urls)} individual web pages...")
            self.process_web_urls(web_urls)
        
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

    def process_pdfs(self, pdf_urls: List[str]) -> None:
        """Process and build knowledge bases from PDFs."""
        for url in pdf_urls:
            try:
                print(f"📄 PDF: {url}")
                path = self.pdf_processor.download(url)
                text = self.pdf_processor.extract_text(path)
                if not text.strip():
                    continue
                self.kbs.append(self.llm.build_kb(text))
            except Exception as e:
                print(f"❌ PDF error: {e}")

    def process_web_urls(self, web_urls: List[str]) -> None:
        """Process and build knowledge bases from individual web URLs."""
        for url in web_urls:
            try:
                print(f"🔗 Website: {url}")
                text = self.website_processor.download_and_clean_html(url)
                if text.strip():
                    self.kbs.append(self.llm.build_kb(text))
            except Exception as e:
                print(f"❌ Website error: {e}")

    def process_websites(self, sitemap_url: str) -> None:
        """Process and build knowledge bases from websites."""
        try:
            print(f"🌐 Sitemap: {sitemap_url}")
            urls = self.website_processor.get_urls_from_sitemap(sitemap_url)
            for url in urls:
                try:
                    print(f"🔗 Website: {url}")
                    text = self.website_processor.download_and_clean_html(url)
                    if text.strip():
                        self.kbs.append(self.llm.build_kb(text))
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