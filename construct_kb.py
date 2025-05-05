import os
import platform
from dotenv import load_dotenv
from knowledge_base_builder import KBBuilder

# === Load .env variables ===
load_dotenv()

def main():
    """Main function to run the knowledge base builder."""
    # API and model configuration
    config = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'GEMINI_MODEL': os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        'GEMINI_TEMPERATURE': float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
        'GITHUB_USERNAME': os.getenv("GITHUB_USERNAME", ""),  # Empty string if not provided
        'GITHUB_API_KEY': os.getenv("GITHUB_API_KEY"),
    }
    
    # Source documents and output configuration
    sources = {
        # PDF Documents
        'pdf_urls': [
            "https://kostadindev.github.io/static/documents/cv.pdf",
            "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
            "file:///C:/Users/kosta/OneDrive/Desktop/MS%20Application%20Materials/emf-ellipse-publication.pdf"
        ],
        
        # Individual Web URLs
        'web_urls': [
            "https://kostadindev.github.io/index.html",
            "https://kostadindev.github.io/projects.html"
        ],
        
        # Sitemap URL for website processing
        'sitemap_url': "https://kostadindev.github.io/sitemap.xml"
    }
    
    # Output file path
    output_file = "final_knowledge_base.md"

    # Create KB builder with API config
    kbb = KBBuilder(config)
    
    # Build knowledge base with sources and output file
    kbb.build_kb(sources=sources, output_file=output_file)

if __name__ == "__main__":
    main()
