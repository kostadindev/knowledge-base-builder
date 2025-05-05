import os
from dotenv import load_dotenv
from kb_app import KnowledgeBaseApp

# === Load .env variables ===
load_dotenv()

def main():
    """Main function to run the knowledge base builder."""
    config = {
        'GOOGLE_API_KEY': os.getenv("GOOGLE_API_KEY"),
        'GEMINI_MODEL': os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        'GEMINI_TEMPERATURE': float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
        'GITHUB_USERNAME': os.getenv("GITHUB_USERNAME", "kostadindev"),
        'GITHUB_API_KEY': os.getenv("GITHUB_API_KEY")
    }
    
    # === Inputs ===
    pdf_urls = [
        "https://kostadindev.github.io/static/documents/cv.pdf",
        "https://kostadindev.github.io/static/documents/sbu_transcript.pdf",
        "file:///C:/Users/kosta/OneDrive/Desktop/MS%20Application%20Materials/emf-ellipse-publication.pdf"
    ]
    sitemap_url = "https://kostadindev.github.io/sitemap.xml"

    # Create and run the app
    app = KnowledgeBaseApp(config)
    app.process_pdfs(pdf_urls)
    app.process_websites(sitemap_url)
    # Uncomment to enable GitHub processing
    # app.process_github()
    app.build_final_kb()

if __name__ == "__main__":
    main()
