from typing import List, Dict, Any
import os
from gemini_client import GeminiClient
from kb_builder import KnowledgeBaseBuilder
from pdf_processor import PDFProcessor
from website_processor import WebsiteProcessor
from github_processor import GitHubProcessor

class KnowledgeBaseApp:
    """Main application class for building knowledge bases from various sources."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.gemini_client = GeminiClient(
            api_key=config['GOOGLE_API_KEY'],
            model=config.get('GEMINI_MODEL', 'gemini-2.0-flash'),
            temperature=float(config.get('GEMINI_TEMPERATURE', 0.7))
        )
        self.kb_builder = KnowledgeBaseBuilder(self.gemini_client)
        self.pdf_processor = PDFProcessor()
        self.website_processor = WebsiteProcessor()
        self.github_processor = GitHubProcessor(
            username=config.get('GITHUB_USERNAME', ''),
            token=config.get('GITHUB_API_KEY')
        )
        self.kbs = []

    def process_pdfs(self, pdf_urls: List[str]) -> None:
        """Process and build knowledge bases from PDFs."""
        for url in pdf_urls:
            try:
                print(f"📄 PDF: {url}")
                path = self.pdf_processor.download(url)
                text = self.pdf_processor.extract_text(path)
                if not text.strip():
                    continue
                self.kbs.append(self.kb_builder.build_kb(text))
            except Exception as e:
                print(f"❌ PDF error: {e}")

    def process_web_urls(self, web_urls: List[str]) -> None:
        """Process and build knowledge bases from individual web URLs."""
        for url in web_urls:
            try:
                print(f"🔗 Website: {url}")
                text = self.website_processor.download_and_clean_html(url)
                if text.strip():
                    self.kbs.append(self.kb_builder.build_kb(text))
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
                        self.kbs.append(self.kb_builder.build_kb(text))
                except Exception as e:
                    print(f"❌ Site error: {e}")
        except Exception as e:
            print(f"❌ Sitemap load error: {e}")

    def process_github(self) -> None:
        """Process and build knowledge bases from GitHub markdown files."""
        try:
            md_urls = self.github_processor.get_markdown_urls()
            for url in md_urls:
                try:
                    print(f"📘 GitHub MD: {url}")
                    text = self.github_processor.download_markdown(url)
                    if text.strip():
                        self.kbs.append(self.kb_builder.build_kb(text))
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
        final_kb = self.kb_builder.recursively_merge_kbs(self.kbs)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_kb)

        print(f"✅ Final KB written to: {output_path}") 